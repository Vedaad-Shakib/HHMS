from django.template import Library

register = Library()

@register.filter
def last_elem(value):
  return value[-1]
