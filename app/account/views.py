import requests
from account.models import PasswordResetToken, User
from article.models import Article
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django_htmx.http import HttpResponseClientRedirect, retarget
from django_htmx.middleware import HtmxDetails
from recipe.models import Recipe

from elisasrecipe import settings

from .forms import ArticleForm, ImageForm, LoginForm, ProfileForm, UserRegistrationForm


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def index(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "index.html",
    )


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


@csrf_exempt
def check_username(request):
    if request.htmx:
        User = get_user_model()
        username = request.POST.get("username")
        if not User.objects.filter(username=username):
            return render(request, "icons/success.html")
        return render(request, "icons/cross.html")


@csrf_exempt
def check_email(request):
    if request.htmx:
        User = get_user_model()
        email = request.POST.get("email")
        if not User.objects.filter(email=email):
            return render(request, "icons/success.html")
        return render(request, "icons/cross.html")


def send_password_reset_email(request):
    if request.htmx:
        email = request.POST["email"]
        try:
            from .models import User

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


@csrf_exempt
def delete_users(request):
    if request.method == "DELETE":
        prefix = "pw_test_"
        users = User.objects.filter(username__startswith=prefix)
        count, _ = users.delete()
        return JsonResponse({"message": f"{count} users deleted."})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)


def get_user_reset_token(request, user_email):
    if settings.DEBUG:
        user = User.objects.get(email=user_email)
        token = PasswordResetToken.objects.get(user=user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return JsonResponse({"token": token.token, "uid": uid})
    return HttpResponse("Endpoint Not for production", status=404)


def profile(request):
    user = request.user
    if user.profile_picture:
        print(user.profile_picture.image)
    else:
        print("no image")
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


def edit_bio(request, field):
    if request.htmx:
        user = request.user
        if field == "first-name":
            if request.GET.get("first-name"):
                user.first_name = request.GET.get("first-name")
            args = {
                "label": "First Name",
                "value": user.first_name,
                "empty_css_class": "first_name_empty",
                "input_css_class": "first_name_input",
            }
        elif field == "image":
            if request.GET.get("first-name"):
                user.first_name = request.GET.get("first-name")
            args = {
                "label": "First Name",
                "value": user.first_name,
                "empty_css_class": "first_name_empty",
                "input_css_class": "first_name_input",
            }
        elif field == "last-name":
            if request.GET.get("last-name"):
                user.last_name = request.GET.get("last-name")
            args = {
                "label": "Last Name",
                "value": user.last_name,
                "empty_css_class": "last_name_empty",
                "input_css_class": "last_name_input",
            }
        elif field == "bio":
            if request.GET.get("bio"):
                user.bio = request.GET.get("bio")
            args = {
                "label": "Bio",
                "value": user.bio,
                "empty_css_class": "bio_empty",
                "input_css_class": "bio_input",
            }
        user.save()
    return render(
        request,
        "components/editable_field.html",
        args,
    )


def authors(request):
    users = User.objects.all()
    return render(
        request,
        "authors.html",
        {"authors": users},
    )


def search_authors(request):
    if request.htmx:
        query = request.GET.get("query")
        users = User.objects.filter(username__icontains=query)
        return render(
            request,
            "components/authors_search_results.html",
            {"authors": users},
        )
    return HttpResponse("Endpoint Not for production", status=404)


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
    recipes = User.favorite_recipes
    return render(
        request,
        "recipe_user_list.html",
        {
            "recipes": recipes,
        },
    )


def user_articles(request):
    form = ArticleForm()
    articles = Article.objects.filter(author=request.user)
    return render(
        request,
        "user_articles.html",
        {"articles": articles, "onwer": True, "form": form},
    )


def edit_image(request):
    if request.htmx:
        print(request.FILES)
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            print("img")
            print(img)
            user = request.user
            user.profile_picture = img
            user.save()
        return """
                <p>image saved</p>
            """
    print(7)
    return HttpResponse("Endpoint for htmx")
