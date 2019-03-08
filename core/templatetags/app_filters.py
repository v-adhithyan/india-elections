import json

from django.template import Library
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = Library()


@register.filter(name='jsonify', is_safe=True)
def jsonify(object):
    return mark_safe(json.dumps(object))


@register.filter(name="link_to_wordcloud", is_safe=True)
def link_to_wordcloud(object):
    return_data = []
    for q in object.split():
        q = q[1:]  # ignore # at index 0
        url = reverse('get-word-cloud') + "?{}={}".format("q", q)
        linked_q = '<a href="{}" style="color:#4D5A85;">#{}</a><br>'.format(url, q)
        return_data.append(format_html(mark_safe(linked_q)))
    return " ".join(return_data)


@register.filter(name="stringify", is_safe=True)
def stringify(object):
    return mark_safe(str(object))
