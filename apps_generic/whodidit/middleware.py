""" Middleware to provide current request user """
from threading import current_thread

from django.utils.deprecation import MiddlewareMixin

_requests = {}


def current_request():
    return _requests.get(current_thread().ident, None)


def get_current_user():
    return current_request().user \
        if hasattr(current_request(), "user") and not \
        current_request().user.is_anonymous else None


class RequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        _requests[current_thread().ident] = request

    def process_response(self, request, response):
        _requests.pop(current_thread().ident, None)
        return response

    def process_exception(self, request, exception):
        _requests.pop(current_thread().ident, None)
        raise exception
