from django import template

register = template.Library()

@register.filter
def user_likes(likes):
    """Extracts user objects from the likes queryset"""
    return [like.user for like in likes]
