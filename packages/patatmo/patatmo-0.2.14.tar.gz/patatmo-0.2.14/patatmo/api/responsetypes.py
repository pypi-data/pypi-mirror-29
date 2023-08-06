#!/usr/bin/env python3
# system modules
import logging

# external modules
import pandas as pd
from pandas import DataFrame
import numpy as np

# internal modules
from patatmo.api.errors import *


class ApiResponse(object):
    """ Base class for Netatmo api response datasets
    """

    def __init__(self, request, response):
        """ Class constructor
        Args:
            request (instance of ApiRequest or derivate): the api request
            response (dict): The raw api response
        """
        self.response = response
        self.request = request

    ##################
    ### Properties ###
    ##################
    @property
    def logger(self):  # pragma: no cover
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
    def response(self):
        """ The raw api response dict.
        """
        try:  # try to return internal attribute
            return self._response
        except AttributeError:  # pragma: no cover
            self._response = {}
        return self._response  # return internal attribute

    @response.setter
    def response(self, newresponse):
        assert isinstance(newresponse, dict), \
            "reponse property has to be of class dict"
        self._response = newresponse

    @property
    def request(self):
        """ The raw api request dict.
        """
        return self._request  # return internal attribute

    @request.setter
    def request(self, newrequest):
        self._request = newrequest

    def __repr__(self):  # pragma: no cover
        """ python representation of this object
        """
        # self.logger.debug("__repr__ called")
        reprstring = ("{classname}(\n"
                      "response = {response},\n"
                      "request = {request},\n"
                      ")").format(
            classname="{module}.{name}".format(
                name=self.__class__.__name__, module=self.__class__.__module__),
            # compact version
            response=self.response.__repr__(),
            # pretty version
            # response = json.dumps(self.response,sort_keys=True,indent=4)
            # the request
            request=self.request.__repr__()
        )
        return reprstring


class TokenResponse(ApiResponse):
    """ Class that holds the responded data of a Oauth2 token request
    """
    pass


class GetpublicdataResponse(ApiResponse):
    """ Class that holds the responded data of a Getstationdata request
    """

    def dataframe(self, only_inside=False):
        """
        Convert the response to a pandas.DataFrame

        Args:
            only_inside (bool, optional): Drop stations outside the requested
                region? Defaults to ``False``.

        Returns:
            pandas.DataFrame: The response converted to a DataFrame
        """
        # get the list of stations
        stations = self.response.get("body")
        if not isinstance(stations, list):  # pragma: no cover
            raise ApiResponseError("'body' part of response does not "
                                   "exist or is no list.")

        # start with basic dict
        stationdict = {
            "id": [],
            "altitude": [],
            "longitude": [],
            "latitude": [],
            "timezone": [],
        }
        # loop over all stations
        for station in stations:
            station_df = DataFrame()  # start with empty DataFrame

            ### gather general information ###
            station_id = station.get("_id", np.nan)
            # add id to dict
            stationdict["id"].append(station_id)

            ### gather positional information ###
            place = station.get("place", {})
            location = place.get("location", [np.nan, np.nan])
            longitude, latitude = location  # get longitude and latitude
            altitude = place.get("altitude", np.nan)
            timezone = place.get("timezone", np.nan)
            # add position to dict
            stationdict["altitude"].append(altitude)
            stationdict["longitude"].append(longitude)
            stationdict["latitude"].append(latitude)
            stationdict["timezone"].append(timezone)

            ### gather measurement information ###
            # loop over all measurements
            measdict = {}
            for module_id, measure in station.get("measures", {}).items():
                types = measure.get("type", [])
                res = measure.get("res", {})  # the time and values
                if not len(res) == 1:  # something is wrong
                    # self.logger.warning("module '{}' has not exactly one time! "
                    #     "Leaving it out.".format(module_id))
                    res = {np.nan: [np.nan] * len(types)}
                timestamp = list(res.keys())[0]
                measurements = res.get(timestamp)
                measdict.update(zip(types, measurements))
                timedict = {"time_{}".format(t): int(timestamp) for t in types}
                measdict.update(timedict)
                # self.logger.debug("measdict after update: {}".format(measdict))

            # add measurements to stationdict
            for key, val in measdict.items():
                try:
                    stationdict[key].append(val)
                except BaseException:
                    stationdict[key] = [val]

            # fill the remaining values
            length = max([len(x) for x in stationdict.values()])
            for key, val in stationdict.items():
                while len(val) < length:
                    val.append(np.nan)

        # create DataFrame
        df = DataFrame(stationdict)
        # convert times to datetime
        for col in df.columns:
            if col.startswith("time_"):
                df[col] = pd.to_datetime(df[col], unit="s", utc=True)

        # drop outliers if desired
        if only_inside:
            lat_ne = self.request.payload["lat_ne"]
            lon_ne = self.request.payload["lon_ne"]
            lat_sw = self.request.payload["lat_sw"]
            lon_sw = self.request.payload["lon_sw"]
            # TODO: What happens in other regions? Is outside still correct?
            outside = np.logical_or(
                df["latitude"] > lat_ne,
                np.logical_or(
                    df["latitude"] < lat_sw,
                    np.logical_or(
                        df["longitude"] > lon_ne,
                        df["longitude"] < lon_sw)))
            # drop outliers
            df.drop(np.where(outside)[0], inplace=True)

        # set index to device id
        if df.id.size != df.id.unique().size:
            self.logger.warning("Duplicate device IDs in the response!")
        df.set_index(df.id, inplace=True)
        # return the resulting DataFrame
        return df


class GetpublicdataMultiResponse(GetpublicdataResponse):
    """ Class that holds responded data of a subdivided Getpublicdata request
    """

    def dataframe(self, only_inside=False):
        """
        Convert the multiple subdivided Getpublicdata responses to a single
        dataframe

        Returns:
            pandas.Dataframe: the merged dataframe
        """
        try:
            count_stations = 0
            responses = self.response.get("parts")
            for response in responses:
                df_cur = response.dataframe(only_inside=only_inside)
                count_stations += df_cur.shape[0]
                try:
                    # join datasets
                    df = pd.concat([df, df_cur], axis=0, join="outer")
                    # df = df.combine_first(df_cur)
                    # drop duplicates
                except NameError:  # first one
                    df = df_cur
            # drop duplicates
            df.drop_duplicates(subset="id", inplace=True)
            return df  # return
        except TypeError:  # not iterable e.g.
            raise ApiResponseError(
                "subdivided Getpublicdata response contains bogus")


class GetmeasureResponse(ApiResponse):
    """ Class that holds the responded data of a Getmeasure request
    """

    def dataframe(self):
        """
        Convert the response to a pandas.DataFrame

        Returns:
            pandas.DataFrame: The response converted to a DataFrame
        """
        body = self.response.get("body")
        if isinstance(body, list):  # optimized # pragma: no cover
            if body:  # only if there really is something
                raise NotImplementedError("converting 'optimized' Getmeasure "
                                          "response is not yet implemented")
            else:
                body = {}  # fake to empty dict
        if isinstance(body, dict):  # unoptimized
            try:
                types = self.request.payload.get(
                    "type").split(",")  # the types
            except AttributeError:  # pragma: no cover
                raise InvalidApiInputError(
                    "There is no sensible 'type' "
                    "section in the request's payload. Strange...")

            # start with empty measurement dict
            measdict = {"time": []}
            # loop over all time-measurement pairs
            for timestamp, measurements in body.items():
                if not len(types) == len(measurements):  # pragma: no cover
                    raise ApiResponseError(
                        "number of requested types does not "
                        "match number of responded types")
                d = dict(zip(types, measurements))
                d.update({"time": int(timestamp)})
                # add measurements to measdict
                for key, val in d.items():
                    try:
                        measdict[key].append(val)
                    except BaseException:
                        measdict[key] = [val]

        else:  # bullshit # pragma: no cover
            raise ApiResponseError("'body' part of response does not "
                                   "exist or is neither list not dict.")

        # create DataFrame
        df = DataFrame(measdict)
        # convert times to datetime
        for col in df.columns:
            if col.startswith("time"):
                df[col] = pd.to_datetime(df[col], unit="s", utc=True)
        # sort the data frame by time
        df = df.sort_values(by="time")
        # index
        df.set_index("time", inplace=True)
        # return the resulting DataFrame
        return df


class GetmeasureMultiResponse(GetmeasureResponse):
    """
    Class holding responded data of multiple Getmeasure requests
    """
    def dataframe(self):
        try:
            responses = self.response.get("parts")
            for response in responses:
                df_cur = response.dataframe()
                try:
                    # join datasets
                    df = pd.concat([df, df_cur], axis=0, join="outer")
                except NameError:  # first one
                    df = df_cur
            # drop duplicates
            df.drop_duplicates(inplace=True)
            # sort
            df.sort_index(inplace=True)
            return df  # return
        except TypeError:  # not iterable e.g.
            raise ApiResponseError(
                "subdivided Getmeasure response contains bogus")

class GetstationsdataResponse(ApiResponse):
    """ Class that holds the responded data of a Getstationsdata request
    """

    def dataframe(self):
        """
        Convert the response to a pandas.DataFrame

        Returns:
            pandas.DataFrame: The response converted to a DataFrame
        """
        body = self.response.get("body")
        if not isinstance(body, dict):  # optimized # pragma: no cover
            raise ApiResponseError("api response body is no dict. Strange...")
        devices = body.get("devices")
        if not isinstance(devices, list):  # no list # pragma: no cover
            raise ApiResponseError("api response devices part is no list. "
                                   "Strange...")
        if len(devices) > 1:  # pragma: no cover
            raise ApiResponseError("api response devices list is longer than "
                                   "one. Strange...")
        try:
            dashboard_data = devices[0]["dashboard_data"]  # device
        except KeyError:  # pragma: no cover
            raise ApiResponseError("api response devices list entry has no "
                                   "dashboard_data")

        # get proper data
        data = {}  # start with empty dict
        for key, val in dashboard_data.items():
            if isinstance(
                    val, dict) or isinstance(
                    val, list):  # pragma: no cover
                raise ApiResponseError("dashboard_data values are not scalars")
            data[key] = [val]  # put it into a list

        # convert to data frame
        df = pd.DataFrame(data)

        # reset index
        df.reset_index(inplace=True)

        return df
