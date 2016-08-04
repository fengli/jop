from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'jop.posts'
    verbose_name = "Posts"

    def ready(self):
        pass
