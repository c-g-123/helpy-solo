from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import UserSettings
from core.forms import UserSettingsForm, UserEmailForm, UsernameForm

def index(request):
    return render(request, 'core/index.html')


@login_required
def account(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    settings_form = UserSettingsForm(instance=user_settings)
    email_form = UserEmailForm(instance=request.user)
    username_form = UsernameForm(instance=request.user)
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'settings':
            settings_form = UserSettingsForm(request.POST, instance=user_settings)

            if settings_form.is_valid():
                settings_form.save()
        
        elif form_type == 'email':
            email_form = UserEmailForm(request.POST, instance=request.user)

            if email_form.is_valid():
                email_form.save()
        
        elif form_type == 'username':
            username_form = UsernameForm(request.POST, instance=request.user)

            if username_form.is_valid():
                username_form.save()
        
    context = {
        'settings_form': settings_form,
        'email_form': email_form,
        'username_form': username_form,
    }

    return render(request, 'core/settings.html', context)
