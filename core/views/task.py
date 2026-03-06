from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.dateparse import parse_datetime

from core.forms import TaskForm
from core.models import Project, Task
from core.views.utils import render_error_message


@login_required
def create_task(request):
    user_projects = Project.objects.filter(user=request.user)

    if request.method == 'GET':
        form = TaskForm(user=request.user)
    elif request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(reverse('core:task', args=[task.id]))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request, 'core/task/create_task.html', {'form': form})


@login_required
def view_task(request, task_id):
    return render(request, 'core/task/task.html')
