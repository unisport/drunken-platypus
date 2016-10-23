from django import template

register = template.Library()


@register.filter(name='make_labels')
@register.inclusion_tag('labels.html')
def make_labels(value):
    labels = value.split(',')
    return {'labels': labels}
