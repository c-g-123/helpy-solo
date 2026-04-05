from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from core.forms import TaskForm
from core.models import Task, Project

from .utility import get_link_chain


@login_required
@require_GET
def create_task(request):
    initial_task = _get_initial_task_from_query_parameters(request)
    return render(request, 'core/pages/create-task.html', {'form': TaskForm(user=request.user, initial=initial_task)})


@login_required
@require_POST
def create_task_submit(request):
    form = TaskForm(user=request.user, data=request.POST)

    if form.is_valid():
        task = form.save()
        return redirect('core:task', task.id)

    return render(request, 'core/pages/create-task.html', {'form': form})


@login_required
@require_GET
def task(request, task_id):
    task = get_object_or_404(Task.objects.for_user(request.user), id=task_id)

    context = {
        'task': task,
        'link_chain': get_link_chain(task),
        'form': TaskForm(user=request.user, instance=task),
        'subtasks': Task.objects.for_parent(task, request.user)
    }

    return render(request, 'core/pages/task.html',context)


@login_required
@require_POST
def edit_task(request, task_id):
    task = get_object_or_404(Task.objects.for_user(request.user), id=task_id)

    form = TaskForm(user=request.user, instance=task, data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('core:task', task.id)

    context = {
        'task': task,
        'breadcrumbs': task.get_breadcrumbs(),
        'form': form,
        'subtasks': Task.objects.for_parent(task, request.user)
    }

    return render(request, 'core/pages/task.html', context)


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task.objects.for_user(request.user), id=task_id)
    task.delete()
    return redirect('core:project', task.project.id)


def _get_initial_task_from_query_parameters(request):
    project_id = request.GET.get('project_id')
    parent_task_id = request.GET.get('parent_task_id')
    raw_due_datetime = request.GET.get('due_datetime')

    initial_task = {}

    if project_id:
        project = get_object_or_404(
            Project,
            id=project_id,
            user=request.user
        )
        initial_task['project'] = project
    if parent_task_id:
        parent_task = get_object_or_404(
            Task,
            id=parent_task_id,
            project__user=request.user
        )
        initial_task['parent_task'] = parent_task
    if raw_due_datetime:
        due_datetime = datetime.fromisoformat(raw_due_datetime)
        initial_task['due_datetime'] = due_datetime

    return initial_task
