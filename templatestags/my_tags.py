from django import template

register = template.Library()
@register.filter(name='get_item')
def get_item(dicti, key):
    return dicti.get(key)