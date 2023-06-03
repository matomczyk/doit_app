"""todo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from doit_app.views import AddTaskView, TaskListView, UpdateTaskView, TaskView, SignUpView, MainPage, BudgetSummaryView, \
                            DeleteTaskView, CompletionSummaryView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('add-task/', AddTaskView.as_view(), name='add-task'),
    path('task-list/', TaskListView.as_view(), name='task-list'),
    path('update-task/<int:pk>/', UpdateTaskView.as_view(), name='update-task'),
    path('task/<int:pk>/', TaskView.as_view(), name='task-details'),
    path('', MainPage.as_view(), name='main'),
    path('budget-summary/', BudgetSummaryView.as_view(), name='budget-summary'),
    path('delete-task/<int:pk>', DeleteTaskView.as_view(), name='delete-task'),
    path('completion-summary/', CompletionSummaryView.as_view(), name='completion-summary')
]
