from django import template

register = template.Library()

@register.filter(name = 'has_status')
def has_status(status):
    status_list = ['Preparing Document']
    return True if status in status_list else False


@register.filter(name = 'under_review_ops')
def under_review_ops(status):
    status_list = ['Submit']
    return True if status in status_list else False


@register.filter(name = 'done_review_ops')
def done_review_ops(status):
    status_list = ['Decline', 'Verified', 'Approve']
    return True if status in status_list else False


@register.filter(name = 'under_review_mgr')
def under_review_mgr(status):
    status_list = ['Verified']
    return True if status in status_list else False


@register.filter(name = 'done_review_mgr')
def done_review_mgr(status):
    status_list = ['Decline', 'Approve', 'Submit']
    return True if status in status_list else False


