from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse

from .utils import render_error_message


def register(request):
    if request.method != 'POST':
        return render(request, 'core/register.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    repeat_password = request.POST.get('repeat_password')

    if not _is_username_valid(username):
        return render_error_message(request, template='core/register.html', error_message='Invalid username.')

    if not _is_password_valid(password, repeat_password):
        return render_error_message(request, template='core/register.html', error_message='Invalid password or the repeat does not match.')

    user = User.objects.create_user(username=username, password=password)

    auth.login(request, user)  # Automatically login. If someone else is already logged in, this logs them out first too.

    return redirect(reverse('core:calendar'))  # WARNING Change this to redirect to the default dashboard chosen by the user.


def login(request):
    if request.method != 'POST':
        return render(request, 'core/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(username=username, password=password)

    if not user:
        return render_error_message(request, template='core/login.html', error_message='Invalid username or password.')

    if not user.is_active:
        return render_error_message(request, template='core/login.html', error_message='Your account is disabled.')

    auth.login(request, user)
    return redirect(reverse('core:calendar'))  # WARNING Change this to redirect to the default dashboard chosen by the user.


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('core:home'))


def _is_username_valid(username):
    if not username:
        return False

    username_already_exists = User.objects.filter(username=username).exists()
    if username_already_exists:
        return False

    return True


def _is_password_valid(password, repeat_password):
    if not password:
        return False

    if password != repeat_password:
        return False

    return True
