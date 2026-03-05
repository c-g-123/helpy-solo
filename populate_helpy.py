import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpy.settings')

import django
django.setup()

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from core.models import Project, Task

def get_or_create_user(username, password):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
    return user

def populate():
    user_1 = get_or_create_user('alice', 'password123')
    user_2 = get_or_create_user('bob', 'password123')

    now = timezone.now()

    project_1_tasks = [
        {'name': 'Setup Django', 
         'description': 'Initialize the project and apps.', 
         'set_date': now, 
         'due_date': now + timedelta(days=2),
         'sub_tasks': [
                {
                    'name': 'Install dependencies', 
                    'description': 'pip install django', 
                    'set_date': now, 
                    'due_date': now + timedelta(days=1)
                },
                {
                    'name': 'Configure settings.py', 
                    'description': 'Set up database and templates.', 
                    'set_date': now, 
                    'due_date': now + timedelta(days=2)
                }
            ]
        },

        {'name': 'Design Database', 
         'description': 'Map out the models and relationships.', 
         'set_date': now, 
         'due_date': now + timedelta(days=4)},
    ]
    
    project_2_tasks = [
        {'name': 'Build Frontend', 
         'description': 'Create HTML templates and CSS.', 
         'set_date': now, 
         'due_date': now + timedelta(days=7)},
        {'name': 'Write Tests', 
         'description': 'Ensure test coverage is above 80%.', 
         'set_date': now + timedelta(days=1), 
         'due_date': now + timedelta(days=10)},
    ]

    projects = {
        'Website Redesign': {'task_data': project_1_tasks, 'user': user_1},
        'Mobile App Launch': {'task_data': project_2_tasks, 'user': user_2},
    }

    for project_name, project_data in projects.items():
        p = add_project(project_name, project_data['user'])

        for task_data in project_data['task_data']:
            parent_task = add_task(
                project_id=p, 
                name=task_data['name'], 
                description=task_data['description'],
                set_date=task_data['set_date'],
                due_date=task_data['due_date']
            )

            if 'sub_tasks' in task_data:
                for sub_task in task_data['sub_tasks']:
                    add_task(
                        project_id=p,
                        name = sub_task['name'],
                        description = sub_task['description'],
                        set_date = sub_task['set_date'],
                        due_date = sub_task['due_date'],
                        parent_task_id = parent_task 
                    )

    for p in Project.objects.all():
        print(f'\nProject: {p.name} (Owner: {p.user_id.username})')

        for t in Task.objects.filter(project_id=p, parent_task_id__isnull=True):
            print(f' -> Task: {t.name}')

            for sub_t in Task.objects.filter(parent_task_id=t):
                print(f' - Sub-task: {sub_t.name}')

def add_task(project_id, name, description, set_date, due_date, parent_task_id=None):
    t, created = Task.objects.get_or_create(
        project_id=project_id, 
        name=name,
        defaults={
            'parent_task_id': parent_task_id,
            'description': description,
            'set_date': set_date,
            'due_date': due_date
        }
    )

    if created:
        t.save()
    return t

def add_project(name, user_id):
    p, created = Project.objects.get_or_create(name=name, user_id=user_id)
    if created:
        p.save()
    return p
    
if __name__ == '__main__':
    print('Starting Helpy population script...')
    populate()
    print('Population finished.')