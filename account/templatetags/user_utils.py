from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name__iexact=group_name).exists()


@register.filter(name='has_permission')
def has_permission(user, permission_name):
    return user.groups.filter(permissions__name__iexact=permission_name).exists()
