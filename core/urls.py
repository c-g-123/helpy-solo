from django.urls import path

from core import views


app_name = 'core'


urlpatterns = [
    path('', views.index, name='index'),

    # Auth

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Aggregation

    path('calendar/', views.calendar, name='calendar'),
    path('agenda/', views.agenda, name='agenda'),
    path('kanban/', views.kanban, name='kanban'),

    # Project

    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project, name='project'),
    path('projects/', views.projects, name='projects'),

    # Task

    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task, name='task'),

    # User

    path('account/', views.settings, name='settings'),
]
