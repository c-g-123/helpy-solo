from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Task

@login_required
def calendar(request):
    return render(request, 'core/calendar.html')


@login_required
def agenda(request):
    # This logic can be changed later on to fit our needs.
    tasks = Task.objects.filter(project_id__user_id=request.user).order_by('due_date') # The double '__' is for project_id -> user_id -> request.user relationship.
    return render(request, 'core/agenda.html', {'tasks': tasks})


@login_required
def kanban(request):
    return render(request, 'core/kanban.html')