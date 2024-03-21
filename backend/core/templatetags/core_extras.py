from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    print(pattern)
    path = request.path
    if path == pattern:
        return 'active'
    return ''
