from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import (
    CustomPasswordResetConfirmView,
    delete_users,
    send_password_reset_email,
    user_favorites,
    user_recipes,
    user_blog,
)

urlpatterns = [
    # Basic auth
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("authors/", views.authors, name="authors"),
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
    # profile menu
    path("user/recipes", user_recipes, name="my-recipes"),
    path("user/blog", user_blog, name="my-blog"),
    path("user/favorites", user_favorites, name="my-favorites"),
    # Profile page
    path("edit-bio/<str:field>", views.edit_bio, name="edit-bio"),
    # path("edit/last-name", views.check_email, name="edit-last-name"),
    # path("edit/bio-name", views.check_email, name="edit-bio-name"),
    # path("edit/facebook", views.check_email, name="edit-facebook"),
    # path("edit/instagram", views.check_email, name="edit-instagram"),
    # path("edit/twitter", views.check_email, name="edit-twitter"),
    # path("edit/youtube", views.check_email, name="edit-youtube"),
    # path("edit/profile-picture", view s.check_email, name="edit-profile-picture"),
]
