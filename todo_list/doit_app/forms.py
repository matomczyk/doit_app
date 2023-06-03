from django import forms
from .models import Task, User, Category, Reminder, TaskTag, Subtask
from django.forms import ModelForm, SelectDateWidget


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

class SelectMonthForm(forms.Form):
    MONTHS = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    )

    month = forms.ChoiceField(choices=MONTHS)

class AddReminderForm(ModelForm):
    class Meta:
        model = Reminder
        fields = ['reminder_time']


class AddTagForm(ModelForm):
    class Meta:
        model = TaskTag
        fields = ['name']


class SearchTagForm(forms.Form):
    tag_name = forms.CharField(max_length=32)


class AddSubtaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'completed']

class UpdateSubtaskForm(ModelForm):
    class Meta:
        model = Subtask
        fields = ['completed']

