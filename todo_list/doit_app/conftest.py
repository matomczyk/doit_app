from django.contrib.auth.models import User
import pytest
from django.test import Client
from doit_app.models import Task, Category
@pytest.fixture
def user():
    user = User.objects.create_user(id=1, username="user", password="")
    return user

@pytest.fixture
def client():
    c = Client()
    return c

@pytest.fixture
def task(user):
    t = Task.objects.create(id=1, name='test name', description='test description', priority=1,
                            estimated_cost=10, start_time='2023-06-01 12:00', category_id=3,
                            user_id=user.id)
    return t

@pytest.fixture
def category():
    c = Category.objects.create(id=12, name='test category', description='test description')
    return c