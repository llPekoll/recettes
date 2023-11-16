from article.models import Article
from common.models import Tag
from django import forms
from django_quill.forms import QuillFormField


class ArticleForm(forms.ModelForm):
    content = QuillFormField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Article
        fields = ["title", "content", "image", "is_draft", "id"]
