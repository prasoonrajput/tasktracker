# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.tasks_list_create, name='task-list-create'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('tasks/summary/', views.tasks_summary, name='task-summary'),
]
