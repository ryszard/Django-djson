from django import template
try:
    import json
except ImportError:
    import simplejson as json

register = template.Library()

@register.filter
def json(value):
    """Return value as a JSON string.

    """
    return json.dumps(value)
