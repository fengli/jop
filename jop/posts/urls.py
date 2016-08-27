# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.post_list,
        name='list'
    ),

    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<slug>\d+)/$',
        view=views.post_detail,
        name='detail'
    ),

    # URL pattern for the UserUpdateView
    url(
        regex=r'^new/$',
        view=views.new_post,
        name='new'
    ),

    url(
        regex=r'^add/comment/post/(?P<slug>\d+)/$',
        view=views.new_meme,
        name='new_meme'
    ),

    url(
        regex=r'^vote/up/meme/(?P<slug>\d+)/$',
        view=views.vote_up_meme,
        name='meme_voteup'
    ),
]
