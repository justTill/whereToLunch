from django import template
register = template.Library()


@register.filter
def index(sequence, position):
    if position < len(sequence):
        return sequence[position]
    else:
        return " "
