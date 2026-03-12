from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from core.forms import ProjectForm
from core.models import Project, Task


@login_required
def create_project(request):
    if request.method == 'GET':
        form = ProjectForm()
    elif request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect(reverse('core:project', args=[project.id]))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request,'core/project/create-project.html', {'form': form})


@login_required
def view_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'GET':
        form = ProjectForm(instance=project)
    elif request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project.save()
            return redirect(reverse('core:projects'))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    tasks = Task.objects.filter(project=project)

    context = {
        'project': project,
        'tasks': tasks,
        'form': form,
    }

    return render(request, 'core/project/project.html', context)


@login_required
def view_projects(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    projects = Project.objects.filter(user=request.user)
    return render(request, 'core/project/projects.html', {'projects': projects})
