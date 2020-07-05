from django import template

register = template.Library()


@register.filter
def line_index(data, line):
    """Line position on dashboard with pagination"""
    return (data.number - 1) * 50 + data.object_list.index(line) + 1
