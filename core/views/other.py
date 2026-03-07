from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import UserSettings
from core.forms import UserSettingsForm

def index(request):
    return render(request, 'core/index.html')


@login_required
def account(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)

        if form.is_valid():
            form.save()
    else:
        form = UserSettingsForm(instance=user_settings)
    
    context = {
        'form': form,
    }

    return render(request, 'core/settings.html', context)
