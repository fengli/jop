from django import template
from django.contrib.auth.models import AnonymousUser

register = template.Library()

@register.simple_tag
def user_votes(post, user=AnonymousUser()):
    if user.is_anonymous():
        return False
    return post.votes.exists(user.id)


@register.inclusion_tag('users/includes/avatar.html')
def avatar(user, size=32, noname=False):
    return dict(user=user, size=size, noname=noname)
