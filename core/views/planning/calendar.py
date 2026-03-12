from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def calendar(request):
    return render(request, 'core/planning/calendar.html')


def month(request):
    return render(request, 'core/planning/calendar.html')
