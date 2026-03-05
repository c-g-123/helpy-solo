from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'core/index.html')


@login_required
def account(request):
    return render(request, 'core/settings.html')
