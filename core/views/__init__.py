from .planning import agenda
from .authentication import register, register_submit, login, login_submit, logout
from .project import create_project, create_project_submit, project, project_submit, projects
from .task import create_task, view_task as task

from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')
