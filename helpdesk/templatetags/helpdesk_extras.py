from django import template

register = template.Library()

@register.filter(name='make_labels')
@register.inclusion_tag('labels.html', takes_context=True)
def make_labels(value):
    labels = value.split(',')
    return {'labels': labels}