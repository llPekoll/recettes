from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_htmx.http import retarget
from django_htmx.middleware import HtmxDetails

from .forms import UserRegistrationForm


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
    return render(request, "register.html", {"form": form})


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
