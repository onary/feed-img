from django.template import Library

register = Library()

@register.filter
def get_height(width, height):
    return round(float(height)/float(width)*200)

@register.filter
def wbr(text):
    if len(text) > 20:
        result = text[0: 20]
        for i in range(20, len(text), 20):
            result += "<wbr>" + text[i:i+20]
        return result
    return text
