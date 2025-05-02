from django import template

register = template.Library()

@register.filter
def abbreviate_position(value):
    mapping = {
        'Асистент': 'аси.',
        'Доцент': 'доц.',
        'Професор': 'проф.',
    }
    return mapping.get(value, value[:4].lower() + '.')