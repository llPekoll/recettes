from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django_htmx.http import retarget
from django_htmx.middleware import HtmxDetails
from django.contrib.auth import authenticate, login

from .forms import UserRegistrationForm, LoginForm


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
    return render(request, "form_register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'form_login.html', {'form': form})



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
