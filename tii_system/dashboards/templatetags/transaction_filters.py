from django import template

register = template.Library()

@register.filter(name = 'incomplete_process')
def incomplete_process(status):
    status_list = ['Draft-us-comp', 'Draft-id-comp', 'Draft-sign-comp']
    return True if status in status_list else False



