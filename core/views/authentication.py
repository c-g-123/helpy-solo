from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse

from core.forms import RegisterForm, LoginForm


def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "core/authentication/register.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=username,
                password=password
            )

            auth.login(request, user)
            return redirect(reverse("core:calendar"))

        return render(request, "core/authentication/register.html", {"form": form})

    return HttpResponseNotAllowed(["GET", "POST"])


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("core:calendar"))

    if request.method == "GET":
        form = LoginForm()
        return render(request, "core/authentication/login.html", {"form": form})

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(request, username=username, password=password)
            auth.login(request, user)

            return redirect(reverse("core:calendar"))

        return render(request, "core/authentication/login.html", {"form": form})

    return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse("core:index"))
