from django.utils.http import urlquote

from http import JSONResponse


class JSONException(Exception):
    def __init__(self, request=None):
        self.request = request

    def to_response(self):
        content={'status': False,
                 'reason': type(self).__name__,}
        if self.request is not None:
            content['next'] = urlquote(self.request.get_full_path())
        return JSONResponse(status=403,
                            content=content)

class LoginRequired(JSONException):
    pass

class ConfigurationRequired(JSONException):
    """The user should execute an additional configuration step to
    access the given resource.

    """
    pass
