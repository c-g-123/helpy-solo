from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


@login_required
def calendar(request):
    return render(request, 'calendar.html')


@login_required
def agenda(request):
    return render(request, 'agenda.html')


@login_required
def kanban(request):
    return render(request, 'kanban.html')


@login_required
def project(request, project_id):
    return render(request, 'project.html')


@login_required
def create_project(request):
    return render(request, 'project.html')


@login_required
def task(request, task_id):
    return render(request, 'task.html')


@login_required
def create_task(request):
    return render(request, 'task.html')


@login_required
def account(request):
    return render(request, 'account.html')
