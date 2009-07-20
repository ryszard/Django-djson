from django.http import HttpResponse

try:
    import json
except ImportError:
    import simplejson as json

class JSONResponse(HttpResponse):
    def __init__(self, content=None, status=None):
        content = json.dumps(content)
        super(JSONResponse, self).__init__(content=content,
                                           status=status,
                                           content_type="application/json")
