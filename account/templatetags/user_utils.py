from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name='has_group')
def has_group(user: User, group_name: str):
    return user.groups.filter(name__iexact=group_name).exists()


@register.filter(name='has_permission')
def has_permission(user, permission_name):
    return user.groups.filter(permissions__name__iexact=permission_name).exists()
