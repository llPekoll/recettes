import requests
from account.forms import LoginForm, ProfileForm, UserRegistrationForm
from account.models import PasswordResetToken, User
from article.models import Article
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_htmx.http import HttpResponseClientRedirect, retarget
from django_htmx.middleware import HtmxDetails
from recipe.models import Recipe

from elisasrecipe import settings


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def register(request):
    if request.htmx:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseClientRedirect("/")
        else:
            print(form.errors)
        return render(
            request,
            "components/register.html",
            {"form": form},
        )
    form = UserRegistrationForm()
    return render(
        request,
        "auth_core.html",
        {"form": form, "step": "register"},
    )


def login_view(request):
    if request.htmx:
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                # TODO refrsh page with error message
                return HttpResponse("user not found")
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseClientRedirect(reverse("home"))
            else:
                print(form.errors)
        return render(
            request,
            "components/login.html",
            {"form": form},
        )
    form = LoginForm()
    return render(
        request,
        "auth_core.html",
        {"form": form, "step": "login"},
    )


def send_password_reset_email(request):
    if request.htmx:
        email = request.POST["email"]
        try:
            from account.models import User

            user = User.objects.get(email=email)

        except User.DoesNotExist:
            rest = render(request, "responses/email_not_found.html")
            return retarget(rest, "#validation-mail-sent")
        token_generator = default_token_generator
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        PasswordResetToken.objects.create(user=user, token=token)

        current_site = get_current_site(request)
        mail_subject = "Reset your password"
        intro = (
            f"Hi {user.username},\n\nTo reset your password, click the link below:\n\n"
        )
        api_key = settings.APIKEY_MAILWIND
        link = f"{current_site}/password-reset/{uid}/{token}/\n\n"
        print(f"{link=}")
        content = render_to_string(
            "emails/password_forgot.html", {"intro": intro, "link": link}
        )
        headers = {"Authorization": "Bearer " + api_key}
        payload = {
            "sender": {"name": "Yohann", "email": "yohann@ymepa.me"},
            "Destinations": [{"email": "yoyo.mepa@gmail.com", "type": "to"}],
            "Subject": mail_subject,
            "Code": content,
        }
        resp = requests.post(
            "https://api.mailwind.io/v1/send", headers=headers, json=payload
        )
        print(resp.status_code)
        return render(
            request, "responses/email_sent.html", {"intro": intro, "link": link}
        )
    else:
        return render(request, "auth_core.html", {"step": "reset-password"})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "components/change_password.html"
    post_reset_login = True
    success_url = reverse_lazy("password-change-success")


def password_change_success(request):
    return render(request, "components/password_change_success.html")


def profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=user)
    return render(
        request,
        "profile.html",
        {"form": form, "user": user},
    )


def authors(request):
    users = User.objects.all()
    return render(
        request,
        "authors.html",
        {"authors": users},
    )


def user_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(
        request,
        "recipe_user_list.html",
        {
            "recipes": recipes,
        },
    )


@login_required
def user_favorites(request):
    recipes = request.user.favorite_recipes.all()
    articles = request.user.favorite_articles.all()
    return render(
        request,
        "user_favorties.html",
        {
            "recipes": recipes,
            "articles": articles,
        },
    )


@login_required
def user_articles(request):
    articles = Article.objects.filter(author=request.user)
    return render(
        request,
        "user_articles.html",
        {"onwer": True, "articles": articles},
    )


@login_required
def author_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    recipes = Recipe.objects.filter(author=user)
    articles = Article.objects.filter(author=user)
    print(recipes)
    print(articles)
    return render(
        request,
        "author_detail.html",
        {
            "user": user,
            "recipes": recipes,
            "articles": articles,
        },
    )
