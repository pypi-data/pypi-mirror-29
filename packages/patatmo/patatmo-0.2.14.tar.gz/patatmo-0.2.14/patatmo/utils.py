#!/usr/bin/env python3
# System modules
import json
import datetime

# External modules

# Internal modules


# Variables
EMPTY_JSON = {}

# read json from a filename


def read_json_from_file(filename):
    """
    read json from a file given then filename
    args:
        filename (str): The path to the file to read
    returns:
        dict, empty dict if error occured during read
    """
    try:  # open and read, return result
        with open(filename, "r") as f:
            return json.load(f)
    except BaseException:  # didn't work, return empty dict
        return {}

# write json to file


def write_json_to_file(data, filename):
    """
    write data to json file
    args:
        filename (str): the json file to write the data to
        data (dict): the data to write to the file
    returns:
        True on success, False otherwise
    """
    try:
        jsonstr = json.dumps(data, sort_keys=True, indent=4)  # try to convert
        # write to file
        with open(filename, "w") as f:
            f.write(jsonstr)
        return True
    except BaseException:
        return False

# get UNIX-timestamp from datetime object


def unix_timestamp(dt):
    """
    Calculate the UNIX-timestamp - i.e. the seconds since 01.01.1970 - from a
    given datetime object

    Args:
        dt (:any:`datetime.datetime`): a datetime object
    Returns:
        float : the UNIX-timestamp in seconds
    """
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

# do nothing


def nothing():  # pragma: no cover
    pass
