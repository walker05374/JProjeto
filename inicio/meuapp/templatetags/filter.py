# seu_app/templatetags/filter.py
from django import template

register = template.Library()

@register.filter
def my_custom_filter(value):
    # Lógica do seu filtro
    return value  # ou qualquer modificação que você queira aplicar
