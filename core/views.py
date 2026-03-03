from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse


def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def calendar(request):
    return render(request, 'calendar.html')


def agenda(request):
    return render(request, 'agenda.html')


def kanban(request):
    return render(request, 'kanban.html')


def project(request, project_id):
    return render(request, 'project.html')


def create_project(request):
    return render(request, 'project.html')


def task(request, task_id):
    return render(request, 'task.html')


def create_task(request):
    return render(request, 'task.html')


def account(request):
    return render(request, 'account.html')


def logout(request):
    auth.logout(request)
    return redirect(reverse('core:home'))
