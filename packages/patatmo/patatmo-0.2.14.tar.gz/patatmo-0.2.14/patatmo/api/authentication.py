#!/usr/bin/env python3
import sys
import json
import re
import os
import logging
import signal
import time
import contextlib

from patatmo import utils
from patatmo.api import requests
from patatmo.api.variables import *
from patatmo.api.errors import *

# constants
EMPTY_TIMES = {
    "read_tokens": 0,
    "write_tokens": 0,
    "update_tokens": 0,
    "change_tmpfile": 0,
    "request_tokens": 0,
    "refresh_tokens": 0,
}

TOKEN_REGEX = re.compile("^[a-z0-9]+\|[a-z0-9]+$")


EMPTY_CREDENTIALS = {
    "password": "",
    "username": "",
    "client_id": "",
    "client_secret": ""
}

EMPTY_TOKEN_REQUEST = {
    "grant_type": "password",
    "password": "",
    "username": "",
    "client_id": "",
    "client_secret": "",
}

EMPTY_TOKEN_REFRESH_REQUEST = {
    "grant_type": "refresh_token",
    "client_id": "",
    "client_secret": "",
    "refresh_token": "",
}

DEFAULT_EXPIRE_TIME = 10800

EMPTY_TOKENS = {"access_token": "", "refresh_token": ""}


class Authentication(object):
    """
    Netatmo api Oauth2 authentication client

    Args:
        credentials (dict of str, optional): developer account credentials.
            Required keys: username, password, cliend_id, client_secret
        tokens (dict of str, optional): the access and refresh token.
            Required keys: access_token, refresh_token
        tmpfile (str, optional): temporary file to use for tokens
    """

    def __init__(self,
                 credentials=EMPTY_CREDENTIALS,
                 tokens=EMPTY_TOKENS,
                 tmpfile=None
                 ):
        self.logger.debug("init: setting credentials...")
        self.credentials = credentials
        self.logger.debug("init: credentials set.")
        self.logger.debug("init: setting tmpfile...")
        self.tmpfile = tmpfile
        self.logger.debug("init: tmpfile set.")

        # only set the (empty) tokens if you didn't already read them from file
        if self.last_token_action != "read_tokens" or tokens != EMPTY_TOKENS:
            self.logger.debug("init: setting tokens...")
            self.tokens = tokens
            self.logger.debug("init: tokens set.")

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
    def credentials(self):
        """ dict of str: The developer account credentials

        If you set this property, it is checked for valid content first.
        """
        try:  # try to return the internal attribute
            return self._credentials
        except AttributeError:  # pragma: no cover
            return EMPTY_CREDENTIALS

    @credentials.setter
    def credentials(self, value):
        assert isinstance(value, dict), "credentials need to be given as dict"
        # check if all needed credentials are there
        for key in EMPTY_CREDENTIALS.keys():
            assert key in value.keys(), \
                "credentials '{}' not defined in new credentials".format(key)
        # set new credentials
        self._credentials = value

    @property
    def tokens(self):
        """ dict of str: The OAuth2 tokens

        If you set this property, it is checked for valid content first.
        Also, automatic saving to the tmpfile occurs if necessary.
        """
        # if there are no tokens yet, set them to empty tokens
        if not hasattr(self, "_tokens"):
            self._tokens = EMPTY_TOKENS

        if self.token_getter_in_progress:  # okay, we don't want recursion
            self.logger.debug(
                "tokens getter: to prevent recursion, don't make "
                "sure tokens are up to date.")
        else:
            self.logger.debug("tokens getter: making sure "
                              "tokens are up to date.")
            with self.no_token_getter_recursion():
                self.make_sure_tokens_are_up_to_date()

        return self._tokens

    @tokens.setter
    def tokens(self, value):
        if self.check_tokens(value):
            # set the new values
            self._tokens = value

            # update the update time
            self.update_time("update_tokens")

            # do tmpfile IO
            self.tmpfile_io()
        else:
            self.logger.info("given tokens have invalid format."
                             "Using empty default.")
            self._tokens = EMPTY_TOKENS

    @property
    def token_getter_in_progress(self):
        """ This is an internal property to prevent recursion in the tokens
        getter. It is always boolean. When you set it, it is converted to bool.
        """
        if hasattr(self, "_token_getter_in_progress"):
            return bool(self._token_getter_in_progress)
        else:
            return False

    @token_getter_in_progress.setter
    def token_getter_in_progress(self, value):
        self._token_getter_in_progress = bool(value)

    @property
    def tmpfile(self):
        """ str: The temporary file for the tokens.

        If you set this property to something DIFFERENT than before, an attempt
        to read tokens from the tmpfile is made. If that fails, the current
        tokens are written to the tmpfile.
        """
        try:
            return self._tmpfile
        except BaseException:
            return None  # defaults to None

    @tmpfile.setter
    def tmpfile(self, value):
        # set the value
        oldtmpfile = self.tmpfile
        if oldtmpfile == value:
            self.logger.debug((
                "Request to set the tmpfile to the same value of '{}'."
                " Not doing anything.").format(value))
            return

        self._tmpfile = value
        self.logger.debug("The tmpfile was changed from '{}' to '{}'.".format(
            oldtmpfile, value))

        # update the tmpfile change time
        self.update_time("change_tmpfile")

        # do tmpfile IO
        self.tmpfile_io()

    ### property checkers ###
    @property
    def tokens_defined(self):
        """ check if the 'tokens' property contains non-empty tokens

        Returns:
            bool: True if tokens are complete, False otherwise
        """
        with self.no_token_getter_recursion():
            res = True
            for key in EMPTY_TOKENS.keys():
                if not TOKEN_REGEX.match(self.tokens.get(key, "")):
                    res = False
        return res

    @property
    def credentials_defined(self):
        """ check if the 'credentials' property contains full credentials

        Returns:
            bool: True if credentials are complete, False otherwise
        """
        res = True
        for key in EMPTY_CREDENTIALS.keys():
            if not self.credentials.get(key):
                res = False
        return res

    @property
    def last_request_time(self):
        """ [read only] The UNIX timestamp of the last new token request
        """
        last_request_time = \
            self.tokens.get("token_request_time",    # try saved time
                            self.token_times.get("request_tokens",  # try internal time
                                                 0  # use default
                                                 ))
        return last_request_time

    @property
    def last_refresh_time(self):
        """ [read only] The UNIX timestamp of the last new token request
        """
        last_refresh_time = \
            self.tokens.get("token_refresh_time",    # try saved time
                            self.token_times.get("refresh_tokens",  # try internal time
                                                 0  # use default
                                                 ))
        return last_refresh_time

    @property
    def expire_time(self):
        """ [read only] The token expire time
        """
        expire_time = self.tokens.get("expire_in",   # try expire_in
                                      self.tokens.get("expires_in",  # else, try expires_in
                                                      DEFAULT_EXPIRE_TIME            # else, use default
                                                      ))
        return expire_time

    @property
    def tokens_are_up_to_date(self):
        """ check if the tokens are up to date

        Returns:
            bool: True if the tokens are still valid, False if they need to be
                updated.
        """
        with self.no_token_getter_recursion():
            now = time.time()  # current time
            if not self.tokens_defined:  # no tokens, not up to date
                return False
            # if the validity time span has been expired
            if self.last_refresh_time + self.expire_time < now and \
               self.last_request_time + self.expire_time < now:
                return False  # not up to date
            else:  # not expired
                return True  # up to date

    ### the specific times ###
    @property
    def token_times(self):
        """ Internal time counter for token-related actions

        Defaults to all times equal to 0.
        """
        try:
            return self._token_times
        except BaseException:
            return EMPTY_TIMES

    @property
    def last_token_action(self):
        """ Determine the last token-related action from token_times property

        Returns the name of the most recent token-related action and None if
        no action has happened yet.
        """
        if self.token_times == EMPTY_TIMES:
            # if nothing was done, return None
            self.logger.debug("There was no token-related action yet.")
            return None
        else:
            # return the most recent action
            action = sorted(                # sort
                self.token_times,         # the token_times
                key=self.token_times.get,  # according to the times
                reverse=True            # in reversed order (newest first)
            )[0]                      # and return the newest element
            self.logger.debug("The last token-related action was '{}'.".format(
                action))
            return action

    ### context managers ###
    @contextlib.contextmanager
    def no_token_getter_recursion(self):
        try:
            old_token_getter_in_progress = self.token_getter_in_progress
            self.logger.debug("recursion-preventer: setting variable to True")
            self.token_getter_in_progress = True
            yield
        finally:
            self.logger.debug(
                "recursion-preventer: resetting variable to {}".format(
                    old_token_getter_in_progress))
            self.token_getter_in_progress = old_token_getter_in_progress

    ###############
    ### Methods ###
    ###############
    def check_tokens(self, tokens):
        """ Check given tokens for completeness and syntax

        Args:
            tokens (dict of str): The tokens to check

        Returns:
            bool: True if tokens are complete, False otherwise
        """
        # check type
        if not isinstance(tokens, dict):
            return False
        # check if all needed credentials are there
        for key in EMPTY_TOKENS.keys():
            if key not in tokens.keys():
                return False
        return True

    def update_time(self, action):
        """ update the internal time for the token-related action 'action'

        Args:
            action (str): the token-related action to update the time for
        """
        self.logger.debug("updating the time for action '{}'".format(action))
        if action not in EMPTY_TIMES.keys():  # pragma: no cover
            raise KeyError
        # update the tmpfile change time
        times = self.token_times.copy()
        times.update({action: time.time()})
        self._token_times = times

    def tmpfile_io(self):
        """ Read or write the tmpfile dependant on what happend last
        Dependant on the last_token_action property, determine read or write
        the tmpfile.
        """
        actions = {
            "change_tmpfile": self.read_tokens_from_tmpfile,
            "update_tokens": self.write_tokens_to_tmpfile,
            "read_tokens": utils.nothing,
            "write_tokens": utils.nothing,
            "request_tokens": utils.nothing,
            "refresh_tokens": utils.nothing,
        }

        last_token_action = self.last_token_action
        # get the appropriate action
        action = actions.get(last_token_action, utils.nothing)
        self.logger.debug("The appropriate action is {}.".format(
            action.__name__))

        # do it!
        success = action()

        # if reading from tmpfile didn't work out, write it
        if action == self.read_tokens_from_tmpfile and not success:
            self.write_tokens_to_tmpfile()

    def read_tokens_from_tmpfile(self):
        """ Read tokens from the tmpfile
        The time for the 'read_tokens'-action is updated on success.

        Returns:
            bool: True if something was actually read from the file into the
                tokens property, False otherwise.
        """
        self.logger.debug("Try reading tokens from tmpfile '{}'....".format(
            self.tmpfile))
        # read
        tokens = utils.read_json_from_file(self.tmpfile)
        # check
        if self.check_tokens(tokens):
            self._tokens = tokens  # set
            self.update_time("read_tokens")  # update time
            self.logger.debug("tokens were read from tmpfile '{}'.".format(
                self.tmpfile))
            return True
        else:
            self.logger.debug("tokens from tmpfile '{}' are invalid.".format(
                self.tmpfile))
            return False

    def write_tokens_to_tmpfile(self):
        """ Write the current tokens to the tmpfile
        The time for the 'write_tokens'-action is updated on success.

        Returns:
            bool: True if something was actually written to file, False
                otherwise.
        """
        with self.no_token_getter_recursion():
            self.logger.debug("Try writing tokens to tmpfile '{}'.".format(
                self.tmpfile))
            # try to write
            success = utils.write_json_to_file(self.tokens, self.tmpfile)
            if success:  # check
                self.logger.debug("tokens written to tmpfile '{}'".format(
                    self.tmpfile))
                self.update_time("write_tokens")  # update time
            else:
                self.logger.debug(
                    "could not write tokens to tmpfile '{}'".format(
                        self.tmpfile))

            return success

    def request_new_tokens(self):
        """ POST a token request to the api OAuth2 server to get NEW tokens
        """
        # check for completeness
        assert self.credentials_defined, \
            "Cannot make a token request with incomplete credentials"

        with self.no_token_getter_recursion():
            payload = EMPTY_TOKEN_REQUEST.copy()  # a copy of an empty request
            payload.update(self.credentials)  # update with credentials
            self.logger.debug("token request payload: {}".format(payload))

            ### create the request ###
            # the request
            tokenrequest = requests.TokenRequest(payload=payload)
            # the response
            tokenresponse = tokenrequest.response

            # check for errors
            error = tokenresponse.response.get("error")
            if error:  # pragma: no cover
                raise API_ERRORS.get(error, ApiResponseError(error))

            tokens = self.tokens.copy()  # a copy of current tokens
            tokens.update(tokenresponse.response)  # update with new data
            tokens.update({"token_request_time": time.time()})
            self.tokens = tokens  # set the updated tokens

            # update the time
            self.update_time("request_tokens")

    def refresh_current_tokens(self):
        """ POST a refresh request to the api OAuth2 server to refresh tokens
        """
        assert self.tokens_defined, \
            "Cannot refresh the tokens with incomplete tokens"

        with self.no_token_getter_recursion():
            ### create the payload ###
            payload = EMPTY_TOKEN_REFRESH_REQUEST.copy()  # a copy of empty request
            # add refresh token
            for key in ("refresh_token",):  # add refresh_token to payload
                payload[key] = self.tokens.get(key)
            for key in (
                "client_id",
                    "client_secret"):  # add credentials to payload
                payload[key] = self.credentials.get(key)
            self.logger.debug(
                "token refresh request payload: {}".format(payload))

            ### create the request ###
            # the request
            tokenrequest = requests.TokenRequest(payload=payload)
            # the response
            tokenresponse = tokenrequest.response

            # check for errors
            error = tokenresponse.response.get("error")
            if error:
                raise API_ERRORS.get(error, ApiResponseError(error))

            tokens = self.tokens.copy()  # a copy of current tokens
            tokens.update(tokenresponse.response)  # update with new data
            tokens.update({"refresh_request_time": time.time()})
            self.tokens = tokens  # set the updated tokens

            # update the time
            self.update_time("refresh_tokens")

    def make_sure_tokens_are_up_to_date(self):
        # """ Make sure the tokens are up to date (if possible)
        # """
        self.logger.debug("I was told to make sure the tokens are up to date.")
        if self.tokens_are_up_to_date:  # check if they are outdated
            self.logger.debug("tokens are already up to date! "
                              "No needed to update anything.")
        else:
            self.logger.debug("tokens are outdated! "
                              "Now let's check if we have credentials.")
            if self.credentials_defined:
                self.logger.debug("Yes, we have credentials and should be able"
                                  " to post requests.")
                if self.tokens_defined:  # there are tokens already
                    self.logger.debug("We already have tokens, let's "
                                      "refresh them.")
                    self.refresh_current_tokens()  # refresh them
                else:  # no tokens yet
                    self.logger.debug("We don't have any tokens yet, let's "
                                      "request new ones.")
                    self.request_new_tokens()  # request new
            else:
                self.logger.debug(
                    "credentials are not defined. I can't do "
                    "anything to make sure the tokens are up to date...")

    def __repr__(self):  # pragma: no cover
        """ python representation of this object
        """
        # self.logger.debug("__repr__ called")
        with self.no_token_getter_recursion():
            reprstring = (
                "{classname}(\n"
                "credentials = {credentials},\n"
                "tokens = {tokens},\n"
                "tmpfile = {tmpfile}\n"
                ")").format(
                classname="{module}.{name}".format(
                    name=self.__class__.__name__,
                    module=self.__class__.__module__),
                credentials=json.dumps(
                    self.credentials,
                    sort_keys=True,
                    indent=8),
                tokens=json.dumps(
                    self.tokens,
                    sort_keys=True,
                    indent=8),
                tmpfile=self.tmpfile if not isinstance(
                    self.tmpfile,
                    str) else '"{}"'.format(
                    self.tmpfile))
        return reprstring
