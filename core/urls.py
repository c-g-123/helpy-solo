from django.urls import path

from core import views


app_name = 'core'


urlpatterns = [
    path('', views.index, name='index'),

    # Auth

    path('register/', views.register, name='register'),
    path('register/submit/', views.register_submit, name='register_submit'),
    path('login/', views.login, name='login'),
    path('login/submit/', views.login_submit, name='login_submit'),
    path('logout/', views.logout, name='logout'),

    # Aggregation

    # path('calendar/', views.calendar, name='calendar'),
    path('agenda/', views.agenda, name='agenda'),
    # path('kanban/', views.kanban, name='kanban'),

    # Project

    path('project/create/', views.create_project, name='create_project'),
    path('project/create/submit/', views.create_project_submit, name='create_project_submit'),
    path('project/<int:project_id>/', views.project, name='project'),
    path('project/<int:project_id>/edit/', views.project_submit, name='project_submit'),
    path('projects/', views.projects, name='projects'),

    # Task

    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task, name='task'),

]
