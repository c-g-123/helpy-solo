from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import Project

@login_required
def create_project(request):

    if request.method != "POST":
        return render(request, 'core/create_project.html')
    
    name = (request.POST.get("name") or "").strip()

    # Validation
    if not name:
        return render(request, 'core/create_project.html', {'error_message': 'Project name is required.'})
    
    Project.objects.create(user_id=request.user, name=name) # Create the project for logged in user

    return redirect(reverse("core:agenda")) # Redirect to agenda for now, can be changed later to project details page

@login_required
def project(request, project_id):
    return render(request, 'core/project.html')
