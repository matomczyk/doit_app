import datetime

from django.test import Client
import pytest
from django.urls import reverse
from doit_app.forms import SelectMonthForm
from django.contrib.auth.models import User
from doit_app.models import Task



def test_main():
    client = Client()
    response = client.get("/")
    assert response.status_code == 200


# Create your tests here.
@pytest.mark.django_db
def test_signup_view_get(client):
    """
    Test the POST request for the SignUpView.
    """
    client = Client()
    response = client.get('/signup/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_signup_view_post_create_user(client) :
    """
    Test the GET request for the SignUpView.
    """
    users = User.objects.count ()
    response = client.post(reverse('signup'), data={
        'username': 'testuser',
        'email': 'user@user.com',
        'password': 'testuserpassword1',
        'repeat_password': 'testuserpassword1',
    })


    assert response.status_code == 302
    assert User.objects.count() == users + 1


@pytest.mark.django_db
def test_add_task_view_requires_login(client):
    """
    Test the GET request for the AddTaskView.
    """
    response = client.get('/add-task/')
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/add-task/"


@pytest.mark.django_db
def test_add_task_view_post(client, user, category):
    """
    Test the POST request for the AddTaskView.
    """
    client.force_login(user=user)
    response = client.get('/add-task/')
    assert response.status_code == 200

    tasks = Task.objects.count()
    payload = {
        'name': 'Test Task',
        'description': 'This is a test task.',
        'priority': 1,
        'category': category.id,
        'estimated_cost': 10,
        'final_cost': 8,
        'start_time': '2023-06-12 12:00',
    }
    response = client.post(reverse('add-task'), data=payload)
    print(response.content)

    assert response.status_code == 302
    assert Task.objects.count() == tasks + 1


@pytest.mark.django_db
def test_task_list_view_requires_login(user, client):
    response = client.get(reverse("task-list"))
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/task-list/"

@pytest.mark.django_db
def test_task_list_view(user, client):
    client.force_login(user=user)
    response = client.get(reverse("task-list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_task_view(user, client, task):
    client.force_login(user=user)
    response = client.get(reverse('update-task', kwargs={"pk": task.id}))
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_task_view_post(user, client, task):
    client.force_login(user=user)
    payload = {
        "completed": 1,
        "final_cost": 12,
        "end_time": "2023-06-03 12:00",
    }
    response = client.post(reverse("update-task", kwargs={"pk": task.id}), data=payload)

    assert response.status_code == 302

    task.refresh_from_db()
    assert task.final_cost == payload["final_cost"]
    assert task.completed == payload["completed"]
    assert task.end_time.strftime("%Y-%m-%d %H:%M") == payload["end_time"]


@pytest.mark.django_db
def test_task_view_get(user, client, task):
    client.force_login(user=user)
    response = client.get(reverse("task-details", kwargs={"pk": task.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_task_view_requires_login(user, client, task):
    response = client.get(reverse("task-details", kwargs={"pk": task.id}))
    assert response.status_code == 302
    assert response.url == f"/accounts/login/?next=/task/{task.id}/"


@pytest.mark.django_db
def test_delete_task_view(user, client, task):
    client.force_login(user=user)
    response = client.get(reverse("delete-task", kwargs={"pk": task.id}))
    assert response.status_code == 200

    tasks = Task.objects.count()
    response = client.post(reverse("delete-task", kwargs={"pk": task.id}))
    assert response.status_code == 302
    assert Task.objects.count() == tasks - 1

@pytest.mark.django_db
def test_budget_summary_view_get(user, client, budget_summary_view):
    """
        Test the GET request for the BudgetSummaryView.
        """
    client.force_login(user=user)
    response = client.get('/budget-summary/')

    assert response.status_code == 200
    assert isinstance(response.context['form'], SelectMonthForm)



