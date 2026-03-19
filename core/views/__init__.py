from .planning import calendar, agenda, kanban
from .authentication import login, register, logout
from .project import create_project, view_project as project, view_projects as projects
from .task import create_task, add_resource, view_task as task
from .user_settings import settings

from django.shortcuts import render, redirect


def index(request):
    return render(request, 'core/index.html')
