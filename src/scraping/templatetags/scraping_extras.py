from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='addstr', is_safe=True)
def addstr(arg1, arg2):
    """Concatenate arg with .png"""
    print(type(arg2))
    return '{root}{label}.png'.format(root=arg1, label=str(arg2).lower())
