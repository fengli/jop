from django.contrib import admin
from jop.posts.models import Post, CachedImage


class PostAdmin(admin.ModelAdmin):
    pass


class CachedImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(CachedImage, CachedImageAdmin)