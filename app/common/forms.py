from django import forms
from django.conf import settings
from django_quill.forms import QuillFormField

from .models import Comment


class CommentForm(forms.ModelForm):
    comment = QuillFormField()
    # id of the content
    # content_id = forms.IntegerField()
    # type of the content
    # content_type = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configs = getattr(settings, "QUILL_CONFIGS", None)
        config = configs["comment"]
        self.fields["comment"].widget.config = config

    class Meta:
        model = Comment
        fields = ["comment"]
