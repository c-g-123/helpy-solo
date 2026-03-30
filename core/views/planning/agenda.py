from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Task


@login_required
def agenda(request):
    tasks = Task.objects.top_level(request.user).order_by('due_datetime')
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
    return render(request, 'core/planning/agenda.html', {'dates': dates.items()})
