from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import (
    CustomPasswordResetConfirmView,
    delete_users,
    send_password_reset_email,
)

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.register, name="profile"),
    path("account/", views.register, name="account"),
    path("check/username", views.check_username, name="validation username"),
    path("check/email", views.check_email, name="validation email"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("reset-password/", send_password_reset_email, name="password-reset"),
    path(
        "password-reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-change-success/",
        views.password_change_success,
        name="password-change-success",
    ),
    # for test
    path("users/delete/", delete_users, name="delete_users"),
]
