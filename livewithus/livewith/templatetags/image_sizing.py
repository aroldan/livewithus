from django import template
register = template.Library()

@register.filter
def get_size_url(imgobj, size):
    return imgobj._get_SIZE_url(size)