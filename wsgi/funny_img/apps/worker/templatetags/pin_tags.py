from django.template import Library

register = Library()

@register.filter
def get_height(width, height):
    return int(round(int(height)/int(width)*200))
