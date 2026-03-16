import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpy.settings')

import django
django.setup()

import random
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from core.models import Project, Task, Tag, Resource


def create_users(n=5):
    users = []
    for i in range(1, n + 1):
        user, created = User.objects.get_or_create(
            username=f"user{i}",
            defaults={"email": f"user{i}@example.com", "password": "pass1234"}
        )
        users.append(user)
    return users


def create_projects(users, n=3):
    projects = []
    for user in users:
        for i in range(1, n + 1):
            project, created = Project.objects.get_or_create(
                user=user,
                name=f"{user.username} Project {i}"
            )
            projects.append(project)
    return projects


def create_tasks(projects, max_depth=2, tasks_per_project=5):
    all_tasks = []

    def add_task(project, parent=None, depth=0):
        if depth > max_depth:
            return None
        task_name = f"Task {len(all_tasks) + 1}"
        task = Task.objects.create(
            project=project,
            parent_task=parent,
            name=task_name,
            description=f"Description for {task_name}",
            set_datetime=datetime.now(),
            due_datetime=datetime.now() + timedelta(days=random.randint(1, 10)),
            status=random.choice([
                Task.Status.TODO,
                Task.Status.IN_PROGRESS,
                Task.Status.DONE
            ])
        )
        all_tasks.append(task)
        # Optionally create subtasks
        for _ in range(random.randint(0, 2)):
            add_task(project, parent=task, depth=depth + 1)

    for project in projects:
        for _ in range(tasks_per_project):
            add_task(project)

    return all_tasks


def create_tags(users, n=5):
    tags = []
    for i in range(1, n + 1):
        tag, created = Tag.objects.get_or_create(name=f"Tag {i}")
        tag.user_tags.set(random.sample(users, k=random.randint(1, len(users))))
        tags.append(tag)
    return tags


def create_resources(tasks, n=3):
    resources = []
    for task in tasks:
        for i in range(n):
            resource = Resource.objects.create(
                task=task,
                name=f"{task.name} Resource {i + 1}",
                added_date=datetime.now()
            )
            resources.append(resource)
    return resources


if __name__ == "__main__":
    users = create_users()
    projects = create_projects(users)
    tasks = create_tasks(projects)
    tags = create_tags(users)
    resources = create_resources(tasks)

    print("Populated database with:")
    print(f"- {len(users)} users")
    print(f"- {len(projects)} projects")
    print(f"- {len(tasks)} tasks")
    print(f"- {len(tags)} tags")
    print(f"- {len(resources)} resources")