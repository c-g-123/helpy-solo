from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from core.forms import ProjectForm

from .utility import get_link_chain


@login_required
@require_GET
def create_project(request):
    initial_project = _get_initial_project_from_query_parameters(request)
    return render(request, 'core/pages/create-project.html', {'form': ProjectForm(user=request.user, initial=initial_project)})


@login_required
@require_POST
def create_project_submit(request):
    form = ProjectForm(user=request.user, data=request.POST)

    if form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        return redirect('core:project', project.id)

    return render(request, 'core/pages/create-project.html', {'form': form})


@login_required
@require_GET
def project(request, project_id):
    project = get_object_or_404(request.user.projects, id=project_id)
    context = {
        'project': project,
        'link_chain': get_link_chain(project),
        'form': ProjectForm(user=request.user, instance=project),
    }
    return render(request, 'core/pages/project.html', context)


@login_required
@require_POST
def edit_project(request, project_id):
    project = get_object_or_404(request.user.projects, id=project_id)

    form = ProjectForm(user=request.user, instance=project, data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('core:project', project_id=project.id)

    return render(request, 'core/pages/project.html', {'form': form})


@login_required
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(request.user.projects, id=project_id)
    project.delete()
    return redirect('core:projects')


@login_required
@require_GET
def projects(request):
    projects = request.user.projects.filter(parent_project=None)
    return render(request, 'core/pages/projects.html', {'projects': projects})

def _get_initial_project_from_query_parameters(request):
    parent_project_id = request.GET.get('parent_project_id')

    initial_project = {}

    if parent_project_id:
        project = get_object_or_404(request.user.projects, id=parent_project_id)
        initial_project['parent_project'] = project

    return initial_project
