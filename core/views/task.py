from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from core.forms import TaskForm, ResourceForm
from core.models import Task, Project


@login_required
def create_task(request):
    initial = {}

    project_id = request.GET.get('project')
    parent_task_id = request.GET.get('parent_task')

    if project_id:
        project = get_object_or_404(
            Project, 
            id=project_id, 
            user=request.user
        )
        initial['project'] = project
    
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
        post_data = request.POST.copy()

        if parent_task_id:
            parent_task = get_object_or_404(
                Task,
                id=parent_task_id,
                project__user=request.user
            )
            post_data['parent_task'] = str(parent_task.id)
            post_data['project'] = str(parent_task.project.id)

        form = TaskForm(post_data, user=request.user)

        if form.is_valid():
            task = form.save()
            return redirect(reverse('core:task', args=[task.id]))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request, 'core/task/create-task.html', {'form': form})

@login_required
def add_resource(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = ResourceForm(request.POST, request.FILES)

    if form.is_valid():
        resource = form.save(commit=False)
        resource.task = task
        resource.save()

    return redirect(reverse('core:task', args=[task.id]))

@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)

    if request.method == 'GET':
        form = TaskForm(instance=task, user=request.user)
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)

        if form.is_valid():
            task = form.save()
            return redirect(reverse('core:agenda'))
    else:
        return HttpResponseNotAllowed(['GET', 'POST']) 

    subtasks = Task.objects.filter(parent_task=task, project__user=request.user)
    breadcrumbs = task.get_breadcrumbs()

    resources = task.resources.all().order_by('-added_date')
    resource_form = ResourceForm()

    context = {
        'task': task,
        'form': form,
        'subtasks': subtasks,
        'breadcrumbs': breadcrumbs,
        'resources': resources,
        'resource_form': resource_form,
    }

    return render(request, 'core/task/task.html', context)
