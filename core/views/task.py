from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.dateparse import parse_datetime

from core.models import Project, Task

@login_required
def create_task(request):
    # Get only the projects that belong to the user, so that they can only assign tasks to their own projects.
    projects = Project.objects.filter(user_id=request.user)

    if request.method != "POST":
        return render(request, 'core/create_task.html', {'projects': projects})

    # Extract and validate form data
    project_id = request.POST.get("project_id")
    name = (request.POST.get("name") or "").strip()
    description = (request.POST.get("description") or "").strip()
    set_date_raw = request.POST.get("set_date")
    due_date_raw = request.POST.get("due_date")

    # Validation
    if not project_id:
        return render(request, 'core/create_task.html', {'projects': projects, 'error_message': 'Please select a project.'})
    
    if not name:
        return render(request, 'core/create_task.html', {'projects': projects, 'error_message': 'Task name is required.'})
    
    if not description:
        return render(request, 'core/create_task.html', {'projects': projects, 'error_message': 'Task description is required.'})

    # Parse the date strings into datetime objects
    set_date = parse_datetime(set_date_raw) if set_date_raw else None
    due_date = parse_datetime(due_date_raw) if due_date_raw else None 

    if not set_date or not due_date:
        return render(request, 'core/create_task.html', {'projects': projects, 'error_message': 'Please provide both dates.'})
    
    # Ensure the selected project belongs to the user
    try:
        project = projects.get(id=project_id)
    except Project.DoesNotExist:
        return render(request, 'core/create_task.html', {'projects': projects, 'error_message': 'Invalid project.'})

    # Create the task
    Task.objects.create(project_id=project, name=name, description=description, set_date=set_date, due_date=due_date)

    return redirect(reverse("core:agenda")) # Redirect to the agenda view

@login_required
def task(request, task_id):
    return render(request, 'core/task.html')
