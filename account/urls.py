from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("account/", views.register, name="account"),
    path("register/check_username", views.check_username, name="validation username"),
    path("register/email", views.check_email, name="validation email"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
