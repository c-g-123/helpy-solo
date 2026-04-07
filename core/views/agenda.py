from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.models import Task


@login_required
@require_GET
def agenda(request):
    tasks = request.user.tasks.filter(parent_task=None).order_by('due_datetime')
    dates = {}

    for task in tasks:
        if task.due_datetime:
            formatted_due_date = task.due_datetime.date().strftime('%A, %d %B %Y')
            if formatted_due_date not in dates:
                dates[formatted_due_date] = {
                    'tasks': [task],
                    'create_task_query': urlencode({
                        'due_datetime': task.due_datetime.date().isoformat(),
                    })
                }
                continue

            dates[formatted_due_date]['tasks'].append(task)

    return render(request, 'core/pages/agenda.html', {'dates': dates.items()})
