import datetime
import calendar as py_calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Task

@login_required
def calendar(request):
    # Get current year and month from URL parameters, default to today.
    today = datetime.date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Handle month wraparound (prev/next navigation).
    if month < 1 or month > 12:
        month = today.month
        year = today.year

    prev_month = 12 if month == 1 else month - 1
    prev_year = year - 1 if month == 1 else year
    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year

    # 2. Fetch tasks for this user, due within this specific month/year
    tasks = Task.objects.filter(
        project__user=request.user,
        due_datetime__year=year,
        due_datetime__month=month,
        parent_task__isnull=True # Only show top-level tasks on the calendar. Subtasks will be shown on the task detail page.
    )

    # 3. Group tasks by their specific day
    tasks_by_day = {}
    for task in tasks:
        if task.due_datetime: # Added a safety check in case a task has no due date
            day = task.due_datetime.day
            if day not in tasks_by_day:
                tasks_by_day[day] = []
            tasks_by_day[day].append(task)

    # 4. Build the calendar matrix (weeks and days)
    cal = py_calendar.Calendar(firstweekday=0) # 0 = Monday
    month_matrix = []
    for week in cal.monthdayscalendar(year, month):
        week_list = []
        for day in week:
            if day == 0:
                week_list.append({'day': 0, 'tasks': []}) # Empty padding days
            else:
                week_list.append({'day': day, 'tasks': tasks_by_day.get(day, [])})
        month_matrix.append(week_list)

    context = {
        'month_matrix': month_matrix,
        'month_name': py_calendar.month_name[month].upper(),
        'year': year,
        'today_day': today.day if today.month == month and today.year == year else None,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'core/planning/calendar.html', context)