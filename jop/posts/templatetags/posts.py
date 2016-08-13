from django import template
from django.contrib.auth.models import AnonymousUser

register = template.Library()

@register.simple_tag
def user_votes(post, user=AnonymousUser()):
    if user.is_anonymous():
        return False
    return post.votes.exists(user.id)
