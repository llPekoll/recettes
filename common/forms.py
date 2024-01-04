from django import forms
from django.conf import settings
from django_quill.forms import QuillFormField

from .models import Comment, Link


class CommentForm(forms.ModelForm):
    comment = QuillFormField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configs = getattr(settings, "QUILL_CONFIGS", None)
        config = configs["comment"]
        self.fields["comment"].widget.config = config

    class Meta:
        model = Comment
        fields = ["comment"]


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ["value", "type", "embedded"]
