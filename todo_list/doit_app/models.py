from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Stores categories for budget summary purposes. Category may be added in django admin
    """
    name = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Task(models.Model):
    """
    Main model storing informations about user tasks. Related to User and Category model.
    """
    PRIORITY_CHOICES = (
        (3, 'Low'),
        (2, 'Medium'),
        (1, 'High'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    start_time = models.DateTimeField(null=False, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)


class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()

    def __str__(self):
        return f"{self.task} - {self.reminder_time}"


class BudgetSummary(models.Model):
    """
    Model that stores budget summary information for each month.
    """
    month = models.CharField(max_length=32)
    total_cost = models.DecimalField(decimal_places=2, max_digits=100)

    def __str__(self):
        return f"{self.month} - Total Cost: {self.total_cost}"


class TaskTag(models.Model):
    """
    Model that stores tags added by user to certain tasks. Model has many-to-many relationship with Task model.
    """
    name = models.CharField(max_length=32)
    task = models.ManyToManyField(Task)

class Subtask(models.Model):
    """
    Model that stores information about smaller tasks related with main Task model.
    Model only allows task name and completion check.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)