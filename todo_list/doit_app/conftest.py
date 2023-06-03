from django.contrib.auth.models import User
import pytest
from django.test import Client
from doit_app.models import Task, Category, Subtask
from doit_app.views import BudgetSummaryView
@pytest.fixture
def user():
    user = User.objects.create_user(id=1, username="user", password="")
    return user

@pytest.fixture
def client():
    c = Client()
    return c

@pytest.fixture
def task(user, category1):
    t = Task.objects.create(id=1, name='test name', description='test description', priority=1,
                            estimated_cost=10, final_cost=8, start_time='2023-06-01 12:00', category_id=category1.id,
                            user_id=user.id)
    return t


@pytest.fixture
def subtask(user):
    s = Subtask.objects.create(id=1, task_id=1, name='test subtask')
    return s
@pytest.fixture
def create_task(user):
    def _create_task(name, priority, category, start_time, estimated_cost, final_cost):
        return Task.objects.create(
            name=name,
            priority=priority,
            category=category,
            start_time=start_time,
            estimated_cost=estimated_cost,
            final_cost=final_cost,
            user=user
        )
    return _create_task

@pytest.fixture
def create_task_completed(user):
    def _create_task_completed(name, priority, category, start_time, estimated_cost, final_cost):
        return Task.objects.create(
            name=name,
            priority=priority,
            completed=1,
            category=category,
            start_time=start_time,
            estimated_cost=estimated_cost,
            final_cost=final_cost,
            user=user
        )
    return _create_task_completed

@pytest.fixture
def category():
    c = Category.objects.create(id=12, name='test category', description='test description')
    return c

@pytest.fixture
def category1():
    c1 = Category.objects.create(id=13, name='test category 2', description='test description')
    return c1



@pytest.fixture
def budget_summary_view():
    return BudgetSummaryView()

@pytest.fixture
def create_category():
    def _create_category(name):
        return Category.objects.create(name=name)
    return _create_category