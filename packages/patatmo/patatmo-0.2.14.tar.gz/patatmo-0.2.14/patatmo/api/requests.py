#!/usr/bin/env python3
# system modules
import logging
import http.client
import urllib
import json
import contextlib

# internal modules
from patatmo import utils
from patatmo.api import responsetypes
from patatmo.api.variables import *
from patatmo.api.errors import *


class ApiRequest(object):
    """ Class for api requests
    """

    def __init__(self, server, url, payload={}):
        """ class constructor
        Args:
            server (str): the server domain
            url (str): the url relative to the server
            payload [Optional(dict)]: the payload
        """
        self.server = server
        self.url = url
        self.payload = payload

    ##################
    ### Properties ###
    ##################
    @property
    def logger(self):
        """ the logging.Logger used for logging.
        Defaults to logging.getLogger(__name__).
        """
        try:  # try to return the internal property
            return self._logger
        except AttributeError:  # didn't work
            return logging.getLogger(__name__)  # return default logger

    @logger.setter
    def logger(self, logger):  # pragma: no cover
        assert isinstance(logger, logging.Logger), \
            "logger property has to be a logging.Logger"
        self._logger = logger

    @property
    def api_connection(self):
        """ The http.client.HTTPSConnection used for server communication.
        You may set this, otherwise a new instance is created automatically on
        first use.
        """
        try:  # try to return the internal attribute
            return self._api_connection
        except AttributeError:  # didn't work
            # set it to new instance
            self._api_connection = http.client.HTTPSConnection(
                NETATMO_API_SERVER)
        # return internal attribute
        return self._api_connection

    @api_connection.setter
    def api_connection(self, newconn):  # pragma: no cover
        if not isinstance(newconn, http.client.HTTPSConnection):
            self.logger.debug(
                "authentication property needs to be of "
                "class HTTPSConnection. Using empty instance instead "
                "of {}.".format(newauth))
            self._api_connection = http.client.HTTPSConnection(
                NETATMO_API_SERVER)
        else:
            self._api_connection = newconn

    @property
    def server(self):
        """ the api server domain
        """
        try:
            return self._server
        except AttributeError:
            return ""  # pragma: no cover

    @server.setter
    def server(self, newserver):
        self._server = str(newserver)

    @property
    def url(self):
        """ the url relative to the server for this api request
        """
        try:
            return self._url
        except AttributeError:
            return ""  # pragma: no cover

    @url.setter
    def url(self, newurl):
        self._url = str(newurl)

    @property
    def payload(self):
        """ the payload to send to the api
        """
        try:
            return self._payload
        except AttributeError:
            return {}  # pragma: no cover

    @payload.setter
    def payload(self, newpayload):
        try:
            assert isinstance(newpayload, dict)
            json.dumps(newpayload)
            urllib.parse.urlencode(newpayload)
        except (TypeError, AssertionError):  # pragma: no cover
            raise InvalidPayloadError("payload has to be a simple dict")
        self._payload = newpayload

    @property
    def payload_urlencoded(self):
        """ [read only] return the urlencoded payload (UTF-8)
        """
        return urllib.parse.urlencode(self.payload, encoding="UTF-8")

    @property
    def response(self):
        """ the api response to this request. Instance of ApiResponse or
        derivates. Issues the request if necessary. You should not set this
        property.
        """
        try:
            return self._response
        except AttributeError:
            self.issue()  # issue the request
        return self._response  # now return

    @response.setter
    def response(self, newresponse):
        try:
            assert issubclass(newresponse.__class__, responsetypes.ApiResponse)
        except (AssertionError, AttributeError):  # pragma: no cover
            raise TypeError("response property has to be instance of "
                            "ApiResponse or derivates.")
        self._response = newresponse

    ########################
    ### context managers ###
    ########################
    @contextlib.contextmanager
    def connection_to_api(self):
        self.connect_to_api()
        try:
            yield
        finally:
            self.close_api_connection()

    ###############
    ### methods ###
    ###############
    def connect_to_api(self):
        """ Connect to the api server
        """
        self.logger.debug("connecting to api server...")
        self.api_connection.connect()  # connect to server
        self.logger.debug("connected to api server.")

    def close_api_connection(self):
        """ Disconnect from the api server
        """
        self.logger.debug("closing connection to api server...")
        self.api_connection.close()  # close the connection
        self.logger.debug("connection to api server closed")

    def post_request(self):
        """ Issue a POST request to the api server on the given url with the
        specified payload.
        Returns:
            response (dict): JSON decoded response data
        """
        with self.connection_to_api():  # connect to api
            self.logger.debug("issuing post request to {u} on server {s} with "
                              "payload {p}".format(s=self.server, u=self.url,
                                                   p=self.payload_urlencoded))
            # POST request to oauth/token
            self.api_connection.request(
                method="POST",                  # a POST request
                url=self.url,                # to this relative url
                body=self.payload_urlencoded,  # with this payload
                headers=PLAIN_URLENCODED_HEADERS  # and this header
            )

            # evaluate output
            response = self.api_connection.getresponse()  # get the responsse
            data = response.read().decode()          # read and decode
            data_json = json.loads(data)                  # load the JSON

            self.logger.debug("api responeded: {}".format(data_json))

        return data_json  # return the json data

    def issue(self):  # pragma: no cover
        """ Issue a POST request to the api server on the given url with the
        specified payload and set the 'response' property to an ApiResponse
        object. Subclasses may override this class to use specific derivates
        of ApiResponse.
        """
        # post the request
        res_data = self.post_request()
        # pack the response into an ApiResponse object
        response = responsetypes.ApiResponse(
            response=res_data, request=self)
        # set the response property
        self.response = response

    def __repr__(self):  # pragma: no cover
        """ python representation of this object
        """
        # self.logger.debug("__repr__ called")
        reprstring = (
            "{classname}(\n"
            "server = {server},\n"
            "url = {url},\n"
            "payload = {payload},\n"
            ")").format(
            classname="{module}.{name}".format(
                name=self.__class__.__name__,
                module=self.__class__.__module__),
            server=self.server.__repr__(),
            url=self.url.__repr__(),
            payload=self.payload.__repr__(),
        )
        return reprstring


class TokenRequest(ApiRequest):
    """ base class for token requests
    """

    def __init__(self, payload={}):
        """ class constructor
        Args:
            payload [Optional(dict)]: the payload
        """
        super().__init__(
            server=NETATMO_API_SERVER,
            url=NETATMO_API_TOKEN_URL,
            payload=payload
        )

    def issue(self):
        """ Issue a POST request to the api server on the Oauth2 endpoint
        with the specified payload and set the 'response' property to an
        TokenResponse object.
        """
        # post the request
        res_data = self.post_request()
        # pack the response into an ApiResponse object
        response = responsetypes.TokenResponse(response=res_data,
                                               request=self)
        # set the response property
        self.response = response


class GetpublicdataRequest(ApiRequest):
    """ class for Getpublicdata requests
    """

    def __init__(self, payload={}):
        """ class constructor
        Args:
            payload [Optional(dict)]: the payload
        """
        super().__init__(
            server=NETATMO_API_SERVER,
            url=NETATMO_API_GETPUBLICDATA_URL,
            payload=payload
        )

    def issue(self):
        """ Issue a POST request to the api server on the Getpublicdata endpoint
        with the specified payload and set the 'response' property to an
        GetpublicdataResponse object.
        """
        # post the request
        res_data = self.post_request()
        # pack the response into an ApiResponse object
        response = responsetypes.GetpublicdataResponse(response=res_data,
                                                       request=self)
        # set the response property
        self.response = response


class GetmeasureRequest(ApiRequest):
    """ class for Getmeasure requests
    """

    def __init__(self, payload={}):
        """ class constructor
        Args:
            payload [Optional(dict)]: the payload
        """
        super().__init__(
            server=NETATMO_API_SERVER,
            url=NETATMO_API_GETMEASURE_URL,
            payload=payload
        )

    def issue(self):
        """ Issue a POST request to the api server on the Getmeasure endpoint
        with the specified payload and set the 'response' property to an
        GetmeasureResponse object.
        """
        # post the request
        res_data = self.post_request()
        # pack the response into an ApiResponse object
        response = responsetypes.GetmeasureResponse(response=res_data,
                                                    request=self)
        # set the response property
        self.response = response


class GetstationsdataRequest(ApiRequest):
    """ class for Getstationsdata requests
    """

    def __init__(self, payload={}):
        """ class constructor
        Args:
            payload [Optional(dict)]: the payload
        """
        super().__init__(
            server=NETATMO_API_SERVER,
            url=NETATMO_API_GETSTATIONSDATA_URL,
            payload=payload
        )

    def issue(self):
        """ Issue a POST request to the api server on the Getstationsdata
        endpoint with the specified payload and set the 'response' property to
        an GetstationsdataResponse object.
        """
        # post the request
        res_data = self.post_request()
        # pack the response into an ApiResponse object
        response = responsetypes.GetstationsdataResponse(response=res_data,
                                                         request=self)
        # set the response property
        self.response = response
