from django import forms
from django.utils.translation import ugettext_lazy as _

class PostForm(forms.Form):
    title = forms.CharField(label=_('title'), help_text = _('an interesting title'))
    description = forms.CharField(label=_('Description'), help_text=_('A short introduction '))
    image_url = forms.URLField(label=_('Image URL'), help_text=_('The image URL'))
    tags = forms.CharField(label=_('Tags'), help_text=_('Tags, split by comma'))
