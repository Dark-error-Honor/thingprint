from django import template

register = template.Library()


def mult(value, arg):
    "Multiplies the arg and the value"
    return value * arg


mult.is_safe = False

register.filter('mult', mult)
