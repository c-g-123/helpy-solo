from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.decorators.http import require_GET, require_POST

from core.forms import RegisterForm, LoginForm
from core.models import UserSettings


@require_GET
def register(request):
    return render(request, "core/pages/register.html", {"form": RegisterForm()})


@require_POST
def register_submit(request):
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )

        user_settings = UserSettings.objects.create(user=user)
        auth.login(request, user)
        return redirect(user_settings.get_default_board_url())

    return render(request, "core/pages/register.html", {"form": form})


@require_GET
def login(request):
    if request.user.is_authenticated:
        return redirect(request.user.usersettings.get_default_board_url())

    return render(request, "core/pages/login.html", {"form": LoginForm()})


@require_POST
def login_submit(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        auth.login(request, form.cleaned_data['authenticated_user'])
        return redirect(form.cleaned_data['authenticated_user'].usersettings.get_default_board_url())

    return render(request, "core/pages/login.html", {"form": form})


@require_POST
def logout(request):
    auth.logout(request)
    return redirect("core:index")
