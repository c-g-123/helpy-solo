from .authorisation import login, register, logout
from .aggregation import calendar, agenda, kanban
from .project import create_project, view_project as project, view_projects as projects
from .task import create_task, view_task as task
from .user import settings

from django.shortcuts import render, redirect


def index(request):
    return render(request, 'core/index.html')
