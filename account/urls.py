from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import delete_users
from .views import PasswordResetConfirmViewCustom, send_password_reset_email

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.register, name="profile"),
    path("account/", views.register, name="account"),
    path("check/username", views.check_username, name="validation username"),
    path("check/email", views.check_email, name="validation email"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("reset-password/", send_password_reset_email, name="reset-password"),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmViewCustom.as_view(),
        name="password_reset_confirm",
    ),
    # for test
    path("users/delete/", delete_users, name="delete_users"),
]
