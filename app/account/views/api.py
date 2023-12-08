import requests
from account.forms import ImageForm
from account.models import PasswordResetToken, User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django_htmx.http import retarget

from elisasrecipe import settings


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


@csrf_exempt
def delete_users(request):
    if settings.DEBUG:
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


@login_required
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
        elif field == "website":
            if request.GET.get("website"):
                user.website = request.GET.get("website")
            args = {
                "label": "Website",
                "value": user.website,
                "empty_css_class": "website_empty",
                "input_css_class": "website_input",
            }
        user.save()
    return render(
        request,
        "components/editable_field.html",
        args,
    )


@login_required
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


@login_required
def edit_image(request):
    if request.htmx:
        form = ImageForm(request.FILES)
        if form.is_valid():
            img = form.save()
            user = request.user
            user.profile_picture[0] = img
            user.save()
        return """
                <p>image saved</p>
            """
    return HttpResponse("Endpoint for htmx")
