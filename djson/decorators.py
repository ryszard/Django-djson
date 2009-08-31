from exceptions import JSONException, LoginRequired
from http import JSONResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required as login_required_old
from django.http import HttpResponse
from functools import wraps

def as_json(function):
    """Serve the returned value as json.

    """
    @wraps(function)
    def wrapper(request, *a, **kw):
        ret = fun(*a, **kw)
        if isinstance(ret, HttpResponse):
            return ret
        return JSONResponse(ret)
    return wrapper

def with_ajax_errors(function):
    """
    If a JSONException is raised and request.is_ajax(), return the result of
    exception.to_response() (a JSONResponse).

    """
    @wraps(function)
    def wrapper(request, *a, **kw):
        if request.is_ajax():
            try:
                return function(request, *a, **kw)
            except JSONException, e:
                return e.to_response()
        else:
            return function(request, *a, **kw)
    return wrapper

def login_required(function):
    """Like django.contrib.auth.decorators.login_required, except that
    if request.is_ajax(), a json response with the approriate
    explanationis returned. This is useful if your site makes heavy
    use of Ajax, when redirects don't make much sense.

    """
    @wraps(function)
    @with_ajax_errors
    def wrapper(request, *a, **kw):
        if not request.is_ajax():

            return login_required_old(function)(request, *a, **kw)
        if request.user.is_authenticated():
            return function(request, *a, **kw)
        else:
            raise LoginRequired(request)
    return wrapper

def ajax_login_required(function):
    @wraps(function)
    @with_ajax_errors
    def wrapper(request, *a, **kw):
        if not request.is_ajax():

            return HttpResponseForbidden("This page is supposed to be called only from an Ajax request.")
        if request.user.is_authenticated():
            return function(request, *a, **kw)
        else:
            raise LoginRequired(request)
    return wrapper
