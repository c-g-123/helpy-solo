from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Task


@login_required
def agenda(request):
    # WARNING Does this actually order by date or does it order alphabetically by the date column?
    tasks = Task.objects.filter(project_id__user_id=request.user).order_by('due_datetime') # The double '__' is for project_id -> user_id -> request.user relationship.

    days_with_tasks = {}

    for task in tasks:
        if task.due_datetime:
            due_date = task.due_datetime.date().strftime('%A, %d %B %Y')
            if due_date not in days_with_tasks:
                days_with_tasks[due_date] = {
                    'due_datetime': task.due_datetime.date(),
                    'tasks': [task],
                }
                continue
            days_with_tasks[due_date]['tasks'].append(task)

    print(days_with_tasks)

    return render(request, 'core/planning/agenda.html', {'days_with_tasks': days_with_tasks.items()})
