from django import forms
from .models import Task, User, Category
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'datetime-local'

class AddTaskForm(ModelForm):
    description = forms.CharField(required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'category', 'estimated_cost', 'start_time']
        widgets = {'start_time': DateInput()}


class UpdateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['completed', 'final_cost', 'end_time']
        widgets = {'end_time': DateInput()}



class SignUpForm(ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.CharField(max_length=254, widget=forms.EmailInput)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
            ]

