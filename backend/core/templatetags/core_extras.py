from django import template
from core.forms import SearchForm
register = template.Library()

@register.simple_tag
def active(request, pattern):
    path = request.path
    if path == pattern:
        return 'active'
    return ''

# @register.simple_tag
# def searchform():
#     return SearchForm()