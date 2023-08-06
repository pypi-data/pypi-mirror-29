#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from cdumay_error import Error, NotImplemented, ValidationError, NotFound


class NotModified(Error):
    """Not Modified"""
    msgid = "HTTP-22313"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=304, message=message, extra=extra)


class Unauthorized(Error):
    """Unauthorized"""
    msgid = "HTTP-28015"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=401, message=message, extra=extra)


class PaymentRequired(Error):
    """Payment Required"""
    msgid = "HTTP-23516"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=402, message=message, extra=extra)


class Forbidden(Error):
    """Forbidden"""
    msgid = "HTTP-29860"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=403, message=message, extra=extra)


class MethodNotAllowed(Error):
    """Method Not Allowed"""
    msgid = "HTTP-00324"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=405, message=message, extra=extra)


class NotAcceptable(Error):
    """Not Acceptable"""
    msgid = "HTTP-30133"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=406, message=message, extra=extra)


class ProxyAuthenticationRequired(Error):
    """Proxy Authentication Required"""
    msgid = "HTTP-32405"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=407, message=message, extra=extra)


class RequestTimeout(Error):
    """Request Time-out"""
    msgid = "HTTP-13821"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=408, message=message, extra=extra)


class Conflict(Error):
    """Conflict"""
    msgid = "HTTP-21124"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=409, message=message, extra=extra)


class Gone(Error):
    """Gone"""
    msgid = "HTTP-15611"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=410, message=message, extra=extra)


class MisdirectedRequest(Error):
    """Misdirected Request"""
    msgid = "HTTP-24099"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=421, message=message, extra=extra)


class InternalServerError(Error):
    """Internal Server Error"""
    msgid = "HTTP-02752"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=500, message=message, extra=extra)


class ProxyError(Error):
    """Proxy Error"""
    msgid = "HTTP-09927"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=502, message=message, extra=extra)


class ServiceUnavailable(Error):
    """Service Unavailable"""
    msgid = "HTTP-26820"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=503, message=message, extra=extra)


class GatewayTimeout(Error):
    """Gateway Time-out"""
    msgid = "HTTP-04192"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=504, message=message, extra=extra)


HTTP_STATUS_CODES = {
    304: NotModified,
    400: ValidationError,
    401: Unauthorized,
    402: PaymentRequired,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    406: NotAcceptable,
    407: ProxyAuthenticationRequired,
    408: RequestTimeout,
    409: Conflict,
    410: Gone,
    421: MisdirectedRequest,
    500: InternalServerError,
    501: NotImplemented,
    502: ProxyError,
    503: ServiceUnavailable,
    504: GatewayTimeout
}


def from_status(status, message=None, extra=None):
    """ Try to create an error from status code

    :param int status: HTTP status
    :param str message: Body content
    :param dict extra: Additional info
    :return: An error
    :rtype: cdumay_rest_client.errors.Error
    """
    if status in HTTP_STATUS_CODES:
        return HTTP_STATUS_CODES[status](message=message, extra=extra)
    else:
        return Error(
            code=status, message=message if message else "Unknown Error",
            extra=extra
        )


def from_response(response, url):
    """ Try to create an error from a HTTP response

    :param request.Response response: HTTP response
    :param str url: URL attained
    :return: An error
    :rtype: cdumay_rest_client.errors.Error
    """
    # noinspection PyBroadException
    try:
        data = response.json()
        if not isinstance(data, dict):
            return from_status(
                response.status_code, response.text,
                extra=dict(url=url, response=response.text)
            )

        code = data.get('code', response.status_code)
        if code in HTTP_STATUS_CODES:
            return HTTP_STATUS_CODES[code].from_json(data)
        else:
            return Error(**data)
    except Exception:
        return from_status(
            response.status_code, response.text,
            extra=dict(url=url, response=response.text)
        )
