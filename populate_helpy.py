import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpy.settings')

import django
django.setup()

import random
from datetime import datetime, timedelta

from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import Project, Task, Resource, UserSettings


def create_users(n=5):
    users = []
    settings_objs = []

    for i in range(1, n + 1):
        user = User(username=f"user{i}", email=f"user{i}@example.com")
        user.set_password("pass1234")
        users.append(user)

    User.objects.bulk_create(users)

    users = list(User.objects.filter(username__startswith="user"))

    for user in users:
        settings_objs.append(UserSettings(user=user))

    UserSettings.objects.bulk_create(settings_objs)

    return users


def create_projects(users, n=3):
    projects = []

    for user in users:
        for i in range(1, n + 1):
            projects.append(Project(
                user=user,
                name=f"{user.username} Project {i}"
            ))

    Project.objects.bulk_create(projects)

    return list(Project.objects.all())


def create_tasks(projects, max_depth=2, tasks_per_project=5):
    all_tasks = []
    now = datetime.now()
    counter = 0

    for project in projects:
        level_tasks = []

        for _ in range(tasks_per_project):
            counter += 1
            task = Task(
                project=project,
                name=f"Task {counter}",
                description=f"Description for Task {counter}",
                set_datetime=now,
                due_datetime=now + timedelta(days=random.randint(1, 10)),
                status=random.choice([
                    Task.Status.TO_DO,
                    Task.Status.IN_PROGRESS,
                    Task.Status.DONE
                ])
            )
            level_tasks.append(task)

        Task.objects.bulk_create(level_tasks)
        created_tasks = list(Task.objects.filter(project=project, parent_task__isnull=True))

        for depth in range(1, max_depth + 1):
            next_level = []

            for parent in created_tasks:
                for _ in range(random.randint(0, 2)):
                    counter += 1
                    child = Task(
                        project=project,
                        parent_task=parent,
                        name=f"Task {counter}",
                        description=f"Description for Task {counter}",
                        set_datetime=now,
                        due_datetime=now + timedelta(days=random.randint(1, 10)),
                        status=random.choice([
                            Task.Status.TO_DO,
                            Task.Status.IN_PROGRESS,
                            Task.Status.DONE
                        ])
                    )
                    next_level.append(child)

            if not next_level:
                break

            Task.objects.bulk_create(next_level)
            created_tasks = next_level  # move down a level
            all_tasks.extend(next_level)

    all_tasks = list(Task.objects.all())
    return all_tasks


def create_resources(tasks, n=3):
    resources = []
    now = datetime.now()

    for task in tasks:
        for i in range(n):
            resources.append(Resource(
                task=task,
                name=f"{task.name} Resource {i + 1}",
                added_date=now
            ))

    Resource.objects.bulk_create(resources)

    return resources


if __name__ == "__main__":
    call_command("flush", verbosity=0, interactive=False)

    users = create_users()
    projects = create_projects(users)
    tasks = create_tasks(projects)
    resources = create_resources(tasks)

    print("Populated database with:")
    print(f"- {len(users)} users")
    print(f"- {len(projects)} projects")
    print(f"- {len(tasks)} tasks")
    print(f"- {len(resources)} resources")
