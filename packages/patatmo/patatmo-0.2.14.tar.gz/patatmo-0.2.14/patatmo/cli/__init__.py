# -*- coding: utf-8 -*-
# System modules
import os
import sys
import argparse
import logging
import configparser

# External modules

# Internal modules
from ..api.client import NetatmoClient
from ..api.authentication import Authentication


def cli_argumentparser(*args, **kwargs):  # pragma: no cover
    """
    Set up and return an :any:`argparse.ArgumentParser` with default arguments
    every patatmo cli script needs.

    Args:
        args (list, optional): further positional arguments handed to the
            constructor
        kwargs (dict, optional): further keyword arguments handed to the
            constructor

    Returns:
        argparse.ArgumentParser: the parser with default arguments
    """
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser.add_argument(
        "-p",
        "--password",
        help="Netatmo developer account password. "
        "Takes precedence over NETATMO_PASSWORD environment variable",
        required=False)
    parser.add_argument(
        "-u",
        "--user",
        help="Netatmo developer account username. "
        "Takes precedence over NETATMO_USERNAME environment variable",
        required=False)
    parser.add_argument(
        "-i",
        "--id",
        help="Netatmo app client id. "
        "Takes precedence over NETATMO_CLIENT_ID environment variable",
        required=False)
    parser.add_argument(
        "-s",
        "--secret",
        help="Netatmo app client secret. "
        "Takes precedence over NETATMO_CLIENT_SECRET environment variable",
        required=False)
    parser.add_argument(
        "-o",
        "--output",
        help="output file. Defaults to '-' which means STDOUT.",
        default="-")
    parser.add_argument(
        "-f",
        "--tmpfile",
        help="temporary authentication file",
        required=False)
    parser.add_argument(
        "--noconfig",
        help="ignore the user's personal "
        "patatmo configuration folder completely",
        required=False,
        default=False,
        action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose output",
                        action="store_true", default=False)
    parser.add_argument("--debug", help="even more verbose output",
                        action="store_true", default=False)
    return parser


def get_credentials(arguments=argparse.Namespace()):  # pragma: no cover
    """
    Try to determine the netatmo credentials in this order:

    1) command-line arguments
    2) environment variables
    3) user configuration folder

    Raise an error if it was not possible to determine all credentials.

    Args:
        arguments (argparse.Namespace, optional): the parsed command-line
            arguments.

    Returns:
        dict : the credentials ready to use by :any:`Authentication`.

    Raises:
        CredentialsError : if any of the credentials could not be determined
    """
    def get_credential(longname, argname, confname, envname):
        try:  # try to get
            value = getattr(arguments, argname)
            return(value.strip())
        except AttributeError:  # user not given via command-line
            value = os.environ.get(envname)
            try:  # check if value is a string
                return(value.strip())
            except AttributeError:  # not given in environment
                try:  # try to read from config file
                    config = get_configuration()  # get user configuration
                    return(config["account"].get(confname).strip())
                except (KeyError, AttributeError):  # not in configuration file
                    methods = []
                    if not arguments == argparse.Namespace():
                        methods.append("command-line argument '{}'".format(
                            argname))
                    methods.append("environment variable '{}'".format(envname))
                    if not (arguments.noconfig
                            if hasattr(arguments, "noconfig") else False):
                        methods.append(
                            "'{}' key in 'accounts' section "
                            "in patatmo user configuration file '{}'".format(
                                confname, get_configuration_file()))
                    if not methods:
                        methods.append("nothing :-) You should not see this.")

                    methodstr = " or ".join(
                        x for x in [", ".join(methods[0:-1]), methods[-1]] if x)
                    message = "Specify {} via {}".format(longname, methodstr)
                    raise CredentialsError(message)

    needed_credentials = [
        ["Netatmo account username", "user", "username", "NETATMO_USERNAME",
            "username"],
        ["Netatmo account password", "password", "password", "NETATMO_PASSWORD",
            "password"],
        ["Netatmo app id", "id", "client_id", "NETATMO_CLIENT_ID", "client_id"],
        ["Netatmo app secret", "secret", "client_secret", "NETATMO_CLIENT_SECRET",
            "client_secret"],
    ]

    credentials = {}
    for longname, argname, confname, envname, resname in needed_credentials:
        credentials[resname] = get_credential(
            longname=longname,
            argname=argname,
            envname=envname,
            confname=confname)

    return credentials


def get_client(arguments=argparse.Namespace()):  # pragma: no cover
    """
    Set up a client for direct usage.

    Args:
        arguments (argparse.Namespace, optional): the parsed command-line
            arguments.

    Returns:
        NetatmoClient : a ready-to-use netatmo api client

    Raises:
        CredentialsError : if any of the credentials could not be determined
    """
    # read credentials
    try:
        credentials = get_credentials(arguments=arguments)
    except CredentialsError as e:
        logging.error(str(e))
        sys.exit(1)

    if not (arguments.noconfig if hasattr(arguments, "noconfig") else False):
        configdir = get_configuration_dir()
        make_sure_dir_exists(configdir)
        tmpfilename = \
            ".{}.json".format(credentials.get("client_id", "auth").strip())
        tmpfile = os.path.join(configdir, tmpfilename)
    else:
        tmpfile = (
            arguments.tmpfile if hasattr(
                arguments,
                "tmpfile") else None)

    # set up a client
    client = NetatmoClient(
        authentication=Authentication(
            credentials=credentials,
            tmpfile=tmpfile,
        ),
    )

    return client


def get_output_file(arguments=argparse.Namespace()):  # pragma: no cover
    """
    Return a file handler according to the 'output' option in the given
    arguments.

    Args:
        arguments (argparse.Namespace, optional): the parsed command-line
            arguments.

    Returns:
        filehandle : the filehandle to output to
    """
    try:
        output = arguments.output
    except AttributeError:
        output = "-"
    return sys.stdout if output == '-' or not output else open(output, "w")


def get_configuration_dir():  # pragma: no cover
    """
    Return the user's configuration directory

    Returns:
        str : path to the user's configueration directory
    """
    return os.path.expanduser("~/.patatmo")


def make_sure_dir_exists(directory):  # pragma: no cover
    """
    Make sure the given directory exists

    Args:
        directory (str): the path of interest
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_configuration_file():  # pragma: no cover
    """
    Return the user's configuration file

    Returns:
        str : path to the user's configueration file
    """
    return os.path.join(get_configuration_dir(), "settings.conf")


def get_configuration():  # pragma: no cover
    """
    Return the user's patatmo configuration

    Returns:
        configparser.ConfigParser: the user's patatmo configuration
    """
    config = configparser.ConfigParser()
    config.read(get_configuration_file())
    return config


class CredentialsError(ValueError):  # pragma: no cover
    pass
