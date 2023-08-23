from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django_htmx.http import HttpResponseClientRedirect, retarget
from django_htmx.middleware import HtmxDetails
import requests
from django.template.loader import render_to_string

from .forms import LoginForm, UserRegistrationForm
from .models import PasswordResetToken


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def index(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "index.html")


def register(request):
    if request.htmx:
        registerform = UserRegistrationForm(request.POST)
        if registerform.is_valid():
            registerform.save()
            return HttpResponseClientRedirect("/")
        else:
            print(registerform.errors)
        return render(
            request,
            "components/register.html",
            {"registerform": registerform},
        )
    form = UserRegistrationForm()
    return render(
        request,
        "auth_core.html",
        {"form": form, "step": "register"},
    )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password.")
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
        api_key = "sw-bxvZ6y19Z3CVsb88NPPajtF0j58x1YxkVBee02tWJxKExYOYg1MTI6XIJau5a"
        link = f"{current_site}/password-reset/{uid}/{token}/\n\n"
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
        return render(
            request, "responses/email_sent.html", {"intro": intro, "link": link}
        )
    else:
        return render(request, "auth_core.html", {"step": "forgot_password"})


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    template_name = "password_reset/reset_password_confirm.html"

    def get(self, request, *args, **kwargs):
        from .forms import ResetForm

        form = ResetForm()
        return render(
            request, "password_reset/reset_password_invalid.html", {"form": form}
        )

    def post(self, request, *args, **kwargs):
        token = kwargs["token"]
        uid = kwargs["uidb64"]
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            token_obj = PasswordResetToken.objects.get(user=user, token=token)
            if default_token_generator.check_token(user, token):
                return super().post(request, *args, **kwargs)
            else:
                return render(request, "password_reset/reset_password_invalid.html")
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            PasswordResetToken.DoesNotExist,
        ) as e:
            return render(request, "password_reset/reset_password_invalid.html")


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User


@csrf_exempt
def delete_users(request):
    if request.method == "DELETE":
        prefix = "pw_test_"
        users = User.objects.filter(username__startswith=prefix)
        count, _ = users.delete()
        return JsonResponse({"message": f"{count} users deleted."})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)
