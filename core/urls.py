from django.urls import path

from core import views

app_name = 'core'


urlpatterns = [
    # Auth

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Other

    path('', views.home, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('agenda/', views.agenda, name='agenda'),
    path('kanban/', views.kanban, name='kanban'),
    path('project/', views.project, name='project'),
    path('project/create', views.create_project, name='create_project'),
    path('task/', views.task, name='task'),
    path('task/create', views.create_task, name='create_task'),
    path('account/', views.account, name='account'),
]
