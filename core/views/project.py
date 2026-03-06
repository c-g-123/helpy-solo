from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse

from core.forms import ProjectForm
from core.models import Project


@login_required
def create_project(request):
    context = {}

    if request.method == 'GET':
        form = ProjectForm()
        context['form'] = form
        return render(request, 'core/create_project.html', context)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        context['form'] = form
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user
            project.save()
            return redirect(reverse('core:project', args=[project.id]))

        return render(request, 'core/create_project.html', context)

    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def view_project(request, project_id):
    project = Project.objects.get(id=project_id, user_id=request.user)
    context = {
        'project': project,
    }

    if request.method == 'GET':
        form = ProjectForm(instance=project)
        context['form'] = form
        return render(request, 'core/project.html', context)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        context['form'] = form
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user
            project.save()
            return redirect(reverse('core:project', args=[project.id]))

        return render(request, 'core/project.html', context)

    return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def view_projects(request):
    projects = Project.objects.filter(user_id=request.user)
    context = {
        'projects': projects
    }

    if request.method == 'GET':
        return render(request, 'core/projects.html', context)

    return HttpResponseNotAllowed(['GET'])
