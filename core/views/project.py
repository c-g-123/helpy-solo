from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from core.forms import ProjectForm
from core.models import Project


@login_required
@require_GET
def create_project(request):
    return render(request, 'core/pages/create-project.html', {'form': ProjectForm()})


@login_required
@require_POST
def create_project_submit(request):
    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        return redirect('core:project', project.id)

    return render(request, 'core/pages/create-project.html', {'form': form})


@login_required
@require_GET
def project(request, project_id):
    project = get_object_or_404(Project.objects.for_user(request.user), id=project_id)
    return render(request, 'core/pages/project.html', {'form': ProjectForm(instance=project)})


@login_required
@require_POST
def project_submit(request, project_id):
    project = get_object_or_404(Project.objects.for_user(request.user), id=project_id)

    form = ProjectForm(request.POST, instance=project)

    if form.is_valid():
        form.save()
        return redirect('core:project', project.id)

    return render(request, 'core/pages/project.html', {'form': form})


@login_required
@require_GET
def projects(request):
    projects = Project.objects.for_user(request.user)
    return render(request, 'core/pages/projects.html', {'projects': projects})
