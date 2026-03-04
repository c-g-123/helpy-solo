from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Project

@login_required
def create_task(request):
    # Get only the projects that belong to the user, so that they can only assign tasks to their own projects.
    projects = Project.objects.filter(user_id=request.user)
    return render(request, 'core/create_task.html', {'projects': projects})


@login_required
def task(request, task_id):
    return render(request, 'core/task.html')
