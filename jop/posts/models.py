import random
import string
import urllib
from django.conf import settings
from django.core.files import File
from django.db import models
from taggit.managers import TaggableManager
import os
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    title = models.TextField(verbose_name=_('Title'), max_length=100, db_index=True)
    slug = models.SlugField(editable=False, db_index=True, unique=True)
    description = models.TextField(verbose_name=_('Description'), max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    cached_image = models.OneToOneField('CachedImage', null=True, blank=True)
    tags = TaggableManager()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        while not self.slug:
            newslug = ''.join(random.choice(string.digits) for _ in range(7))

            if not Post.objects.filter(slug=newslug).count():
                self.slug = newslug

        super(Post, self).save(*args, **kwargs)


class CachedImage(models.Model):
    image_url = models.URLField()
    image_file = models.ImageField(upload_to='images', blank=True)

    def save(self, *args, **kwargs):
        self.cache()
        super(CachedImage, self).save(*args, **kwargs)

    def cache(self):
        """Store image locally if we have a URL"""
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            name = os.path.basename(self.image_url)
            __, ext = os.path.splitext(name)
            newname = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(10)) + ext
            self.image_file.save(
                newname,
                File(open(result[0]))
            )