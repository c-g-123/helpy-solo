from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth

from core.models import UserSettings
from core.forms import UserSettingsForm, UserEmailForm, UsernameForm


@login_required
def settings(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    settings_form = UserSettingsForm(instance=user_settings)
    email_form = UserEmailForm(instance=request.user)
    username_form = UsernameForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'settings':
            settings_form = UserSettingsForm(request.POST, instance=user_settings)

            if settings_form.is_valid():
                settings_form.save()
                return redirect('core:settings')

        elif form_type == 'email':
            email_form = UserEmailForm(request.POST, instance=request.user)

            if email_form.is_valid():
                email_form.save()
                return redirect('core:settings')

        elif form_type == 'username':
            username_form = UsernameForm(request.POST, instance=request.user)

            if username_form.is_valid():
                username_form.save()
                return redirect('core:settings')

        elif form_type == 'password':
            password_form = PasswordChangeForm(user=request.user, data=request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in after password change.
                return redirect('core:settings')

        elif form_type == 'delete_account':
            user = request.user
            auth.logout(request)
            user.delete()
            return redirect('core:index')

    context = {
        'settings_form': settings_form,
        'email_form': email_form,
        'username_form': username_form,
        'password_form': password_form,
    }

    return render(request, 'core/user/pages/settings.html', context)
