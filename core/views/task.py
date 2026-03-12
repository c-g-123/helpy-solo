from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from core.forms import TaskForm
from core.models import Task


@login_required
def create_task(request):
    initial = {}

    parent_task_id = request.GET.get('parent_task')
    if parent_task_id:
        parent_task = get_object_or_404(
            Task,
            id=parent_task_id,
            project__user=request.user
        )
        initial['parent_task'] = parent_task
        initial['project'] = parent_task.project

    if request.method == 'GET':
        form = TaskForm(user=request.user, initial=initial)
    elif request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save()
            return redirect(reverse('core:task', args=[task.id]))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request, 'core/task/create-task.html', {'form': form})


@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)

    if request.method == 'GET':
        form = TaskForm(instance=task, user=request.user)
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)

        if form.is_valid():
            task = form.save()
            return redirect(reverse('core:task', args=[task.id]))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    subtasks = Task.objects.filter(parent_task=task, project__user=request.user)

    context = {
        'task': task,
        'form': form,
        'subtasks': subtasks,
    }

    return render(request, 'core/task/task.html', context)
