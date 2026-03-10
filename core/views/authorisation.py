from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse

from .utils import render_error_message
from ..forms import RegisterForm, LoginForm


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
        return render(request, 'core/authorisation/pages/register.html', {'form': form})

    form = RegisterForm(request.POST)

    if form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        auth.login(request, user)
        return redirect(reverse("core:calendar"))

    return render(request, 'core/authorisation/pages/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("core:calendar"))

    if request.method != "POST":
        form = LoginForm()
        return render(request, 'core/authorisation/pages/login.html', {'form': form})

    form = LoginForm(request.POST)

    if form.is_valid():
        auth.login(request, form.cleaned_data["authenticated_user"])
        return redirect(reverse("core:calendar"))

    return render(request, "core/authorisation/pages/login.html", {"form": form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('core:index'))
