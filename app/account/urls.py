from account.views.api import (
    check_email,
    check_username,
    delete_users,
    edit_bio,
    edit_image,
)
from account.views.page import (
    CustomPasswordResetConfirmView,
    author_detail,
    authors,
    login_view,
    password_change_success,
    profile,
    register,
    send_password_reset_email,
    user_articles,
    user_favorites,
    user_recipes,
)
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "user"

urlpatterns = [
    # page
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("authors/", authors, name="authors"),
    path("author/<int:pk>", author_detail, name="detail"),
    path("account/", profile, name="account"),
    path("login/", login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("reset-password/", send_password_reset_email, name="password-reset"),
    path(
        "password-reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-change-success/",
        password_change_success,
        name="password-change-success",
    ),
    path("user/recipes", user_recipes, name="my-recipes"),
    path("user/articles", user_articles, name="my-articles"),
    path("user/favorites", user_favorites, name="my-favorites"),
    # API
    path("users/delete/", delete_users, name="api-delete-users"),
    path("check/username", check_username, name="api-validation-username"),
    path("check/email", check_email, name="api-validation email"),
    path("edit-bio/image/", edit_image, name="api-edit-image"),
    path("edit-bio/<str:field>", edit_bio, name="api-edit-bio"),
]
