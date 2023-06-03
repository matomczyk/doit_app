import datetime
import calendar

from django.test import Client
import pytest
from django.urls import reverse
from doit_app.forms import SelectMonthForm
from django.contrib.auth.models import User
from doit_app.models import Task, Subtask



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
def test_budget_summary_view_get(user, client):
    """
        Test the GET request for the BudgetSummaryView.
        """
    client.force_login(user=user)
    response = client.get('/budget-summary/')

    assert response.status_code == 200
    assert isinstance(response.context['form'], SelectMonthForm)

@pytest.mark.django_db
def test_budget_summary_view_post(client, user, category, category1, create_task):
    """
    Test the POST request for the BudgetSummaryView.
    """
    client.force_login(user=user)
    task1 = create_task("Test1", 1, category, datetime.date.today(), 10, 8)
    task2 = create_task("Test2", 2, category1, datetime.date.today(), 11, 3)
    task1.refresh_from_db()
    task2.refresh_from_db()
    chosen_month = 6
    response = client.post(reverse('budget-summary'), data={"month": chosen_month})

    assert response.status_code == 200
    assert response.context['chosen_month'] == calendar.month_name[chosen_month]
    assert response.context['total'].month == calendar.month_name[chosen_month]

    summary = response.context['summary']
    assert len(summary) == 12

    summary_item1 = summary[-2]
    assert summary_item1['category'] == category
    assert summary_item1['estimated'] == 10
    assert summary_item1['final'] == 8
    assert summary_item1['variance'] == 2

    summary_item2 = summary[-1]
    assert summary_item2['category'] == category1
    assert summary_item2['estimated'] == 11
    assert summary_item2['final'] == 3
    assert summary_item2['variance'] == 8

    total = response.context['total']
    assert total.month == calendar.month_name[chosen_month]
    assert total.total_cost == 11

@pytest.mark.django_db
def test_completion_summary_view_get(user, client):
    """
        Test the GET request for the CompletionSummaryView.
        """
    client.force_login(user=user)
    response = client.get('/completion-summary/')

    assert response.status_code == 200
    assert isinstance(response.context['form'], SelectMonthForm)



@pytest.mark.django_db
def test_completion_summary_view_post(client, user, category, category1, create_task, create_task_completed):
    """
    Test the POST request for the BudgetSummaryView.
    """
    client.force_login(user=user)
    task1 = create_task("Test1", 1, category, datetime.date.today(), 10, 8)
    task2 = create_task("Test2", 2, category1, datetime.date.today(), 11, 3)
    task3 = create_task_completed("Test3", 2, category1, datetime.date.today(), 1, 3)
    task4 = create_task_completed("Test4", 2, category, datetime.date.today(), 1, 0)
    chosen_month = 6
    response = client.post(reverse('completion-summary'), data={"month": chosen_month})

    assert response.status_code == 200
    assert response.context['chosen_month'] == calendar.month_name[chosen_month]

    if response.context.get('no_task'):
        assert response.context['no_task'] == "Seems like you haven't added any tasks yet."
    else:
        if response.context.get('message'):
            assert response.context[
                       'message'] == "Congratulations! You have completed 66.67% of your tasks this month, great job!"
        elif response.context.get('summary'):
            assert response.context['summary'] == "50.00%"


@pytest.mark.django_db
def test_add_subtask_view_requires_login(client, task):
    """
    Test the GET request for the AddTaskView.
    """
    response = client.get(reverse("subtask", kwargs={"pk": task.id}))
    assert response.status_code == 302
    assert response.url == f"/accounts/login/?next=/add-subtask/{task.id}"


# @pytest.mark.django_db
# def test_update_subtask_view(user, client, task):
#     client.force_login(user=user)
#     response = client.get(reverse("update-subtask", kwargs={"pk": task.id}))
#     assert response.status_code == 200

@pytest.mark.django_db
def test_add_task_tag_view(user, client, task):
    client.force_login(user=user)

    response = client.post(reverse(('tag'), kwargs={"pk": task.id}), data={'name': 'New Tag'})
    assert response.status_code == 302
    assert response.url == '/task-list/'

    # Verify that the task tag was added to the task
    task.refresh_from_db()
    assert task.tasktag_set.count() == 1
    assert task.tasktag_set.first().name == 'New Tag'

@pytest.mark.django_db
def test_update_subtask_view_post(user, client, subtask, task):
    client.force_login(user=user)
    payload = {
        "completed": 1,
    }
    response = client.post(reverse("update-subtask", kwargs={"pk": task.id}), data=payload)

    assert response.status_code == 302

    subtask.refresh_from_db()
    assert subtask.completed == payload["completed"]


# @pytest.mark.django_db
# def test_add_subtask_view_post(client, user, task):
#     """
#     Test the POST request for the AddTaskView.
#     """
#     client.force_login(user=user)
#     response = client.get(reverse('add_subtask', args={"pk": task.id}))
#     assert response.status_code == 200
#
#     subtasks = Subtask.objects.count()
#     payload = {
#         'name': 'Test Subtask 2',
#     }
#     response = client.post(reverse('subtask'), data=payload)
#
#     assert response.status_code == 302
#     assert Task.objects.count() == subtasks + 1

@pytest.mark.django_db
def test_task_subtasks_view(user, client, task, subtask):
    client.force_login (user=user)
    response = client.get(reverse('task-subtasks', kwargs={'pk': task.pk}))

    assert response.status_code == 200
    assert 'task' in response.context
    assert 'subtasks' in response.context
    assert response.context['task'] == task
    assert list(response.context['subtasks']) == [subtask]




