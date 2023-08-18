from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django_htmx.http import HttpResponseClientRefresh, retarget
from django_htmx.middleware import HtmxDetails

from .forms import LoginForm, UserRegistrationForm


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def index(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "index.html")


def register(request):
    if request.htmx:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("htmx request!")
        resp = render(request, "form.html", {"form": form})
        return retarget(resp, "#form-register")

    form = UserRegistrationForm()
    return render(request, "auth_core.html", {"form": form, "login": False})


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
    else:
        form = LoginForm()
    return render(request, "auth_core.html", {"form": form, "login": True})


def check_username(request):
    if request.htmx:
        User = get_user_model()
        username = request.POST.get("username")
        if not User.objects.filter(username=username):
            return HttpResponse("Good")
        return HttpResponse("Not Good")


def check_email(request):
    if request.htmx:
        User = get_user_model()
        email = request.POST.get("email")
        if not User.objects.filter(email=email):
            return HttpResponse("Good")
        return HttpResponse("Not Good")
