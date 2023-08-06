#!/usr/bin/env python3
# module for api errors

##############
### Errors ###
##############


class ApiResponseError(BaseException):
    pass


class InvalidCredentialsError(ApiResponseError):
    pass


class InvalidApiInputError(BaseException):
    pass


class InvalidRegionError(InvalidApiInputError):
    def __init__(self):
        message = \
            ("'region' required keys: "
             "lat_ne [-85;85], lat_sw [-85;85], "
             "lon_ne [-180;180] and lon_sw [-180;180] "
             "with lat_ne > lat_sw and lon_ne > lon_sw")
        super().__init__(message)


class InvalidRequiredDataError(InvalidApiInputError):
    def __init__(self):
        message = "'required_data' must be None or in {}".format(
            GETPUBLICDATA_ALLOWED_REQUIRED_DATA)
        super().__init__(message)


class InvalidApiRequestInputError(BaseException):
    pass


class InvalidPayloadError(InvalidApiRequestInputError):
    pass


API_ERRORS = {
    "invalid_client": InvalidCredentialsError("wrong credentials"),
    "invalid_request": ApiResponseError("invalid request"),
    "invalid_grant": ApiResponseError("invalid grant"),
    "Device not found": ApiResponseError("Device not found - Check Device ID "
                                         "and permissions")
}
