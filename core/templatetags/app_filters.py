import json

from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


def jsonify(object):
    return mark_safe(json.dumps(object))


register.filter('jsonify', jsonify)
jsonify.is_safe = True
