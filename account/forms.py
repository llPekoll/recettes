from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "text-gray-900 rounded-lg border-none bg-gray-200 border-transparent focus:border-transparent focus:ring-0 "
                }
            ),
            "email": forms.TextInput(attrs={"class": "form-control"}),
        }
