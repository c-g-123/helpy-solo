from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Task


@login_required
def kanban(request):

    tasks_todo = Task.objects.top_level_to_do(request.user)
    tasks_in_progress = Task.objects.top_level_in_progress(request.user)
    tasks_done= Task.objects.top_level_done(request.user)

    context = {
        'tasks_todo': tasks_todo,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done
        }

    return render(request, 'core/planning/kanban.html', context)
