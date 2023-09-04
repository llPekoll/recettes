from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import (
    CustomPasswordResetConfirmView,
    delete_users,
    send_password_reset_email,
)

urlpatterns = [
    # Basic auth
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("account/", views.profile, name="account"),
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
    # HTMX
    path("check/username", views.check_username, name="validation username"),
    path("check/email", views.check_email, name="validation email"),
    # Profile page
    path("add/first-name", views.check_email, name="add-first-name"),
    path("add/last-name", views.check_email, name="add-last-name"),
    path("add/bio-name", views.check_email, name="add-bio-name"),
    path("add/facebook", views.check_email, name="add-facebook"),
    path("add/instagram", views.check_email, name="add-instagram"),
    path("add/twitter", views.check_email, name="add-twitter"),
    path("add/youtube", views.check_email, name="add-youtube"),
    path("add/profile-picture", views.check_email, name="add-profile-picture"),
]
