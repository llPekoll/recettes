from account.models import ProfileImage, User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_quill.forms import QuillFormField


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=[
            "Your password must contain at least 8 characters.",
            "Your password must not be too similar to your other personal information.",
            "Your password must not be a commonly used password.",
            "Your password must not be entirely numeric.",
        ],
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class ResetForm(forms.Form):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=[
            "Your password must contain at least 8 characters.",
            "Your password must not be too similar to your other personal information.",
            "Your password must not be a commonly used password.",
            "Your password must not be entirely numeric.",
        ],
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "youtube_handle",
            "twitter_handle",
            "instagram_handle",
            "facebook_handle",
            "website",
            "favorite_recipes",
        )
        widgets = {
            "favorite_recipes": forms.CheckboxSelectMultiple(),
        }


from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    content = QuillFormField(required=False)

    class Meta:
        model = Article
        fields = ["title", "content", "image"]


class ImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = ProfileImage
        fields = ["image"]
