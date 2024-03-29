from article.models import Article
from django import forms
from django.conf import settings
from django_quill.forms import QuillFormField


class ArticleForm(forms.ModelForm):
    content = QuillFormField(required=False)
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configs = getattr(settings, "QUILL_CONFIGS", None)
        config = configs["article"]
        self.fields["content"].widget.config = config

    class Meta:
        model = Article
        fields = ["title", "content", "is_draft", "id", "is_published"]
