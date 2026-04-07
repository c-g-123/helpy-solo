from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from core.forms import TaskForm
from core.models import Task, Project

from .utility import get_link_chain
from ..forms.recurrence_rule import RecurrenceRuleForm


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
    task = get_object_or_404(request.user.tasks, id=task_id)

    recurrence_rule = getattr(task, 'recurrence_rule', None)

    context = {
        'task': task,
        'link_chain': get_link_chain(task),
        'forms': {
            'task': TaskForm(user=request.user, instance=task),
            'recurrence_rule': RecurrenceRuleForm(instance=recurrence_rule),
        }
    }

    return render(request, 'core/pages/task.html',context)


@login_required
@require_POST
def edit_task(request, task_id):
    task = get_object_or_404(request.user.tasks, id=task_id)
    task_form = TaskForm(user=request.user, instance=task, data=request.POST)

    recurrence_rule = getattr(task, 'recurrence_rule', None)
    recurrence_enabled = request.POST.get('recurrence_enabled') == 'on'
    recurrence_form = RecurrenceRuleForm(
        instance=recurrence_rule,
        data=request.POST if recurrence_enabled else None
    )

    recurrence_form_valid = recurrence_form.is_valid() if recurrence_enabled else True

    if task_form.is_valid() and recurrence_form_valid:
        task_form.save()
        if recurrence_enabled:
            rule = recurrence_form.save(commit=False)
            rule.base_task = task
            rule.save()
        elif recurrence_rule:
            recurrence_rule.delete()
        return redirect('core:task', task.id)

    context = {
        'task': task,
        'link_chain': get_link_chain(task),
        'forms': {
            'task': task_form,
            'recurrence_rule': recurrence_form,
        }
    }
    return render(request, 'core/pages/task.html', context)


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(request.user.tasks, id=task_id)
    task.delete()
    return redirect('core:project', task.project.id)


def _get_initial_task_from_query_parameters(request):
    project_id = request.GET.get('project_id')
    parent_task_id = request.GET.get('parent_task_id')
    raw_due_datetime = request.GET.get('due_datetime')

    initial_task = {}

    if project_id:
        project = get_object_or_404(request.user.projects, id=project_id)
        initial_task['project'] = project
    if parent_task_id:
        parent_task = get_object_or_404(request.user.tasks, id=parent_task_id)
        initial_task['parent_task'] = parent_task
    if raw_due_datetime:
        due_datetime = datetime.fromisoformat(raw_due_datetime)
        initial_task['due_datetime'] = due_datetime

    return initial_task
