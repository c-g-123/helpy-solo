from django.urls import path

from core import views


app_name = 'rango'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('calendar/', views.calendar, name='calendar'),
    path('agenda/', views.agenda, name='agenda'),
    path('kanban/', views.kanban, name='kanban'),
    path('project/', views.project, name='project'),
    path('project/create', views.create_project, name='create_project'),
    path('task/', views.task, name='task'),
    path('task/create', views.create_task, name='create_task'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),
]
