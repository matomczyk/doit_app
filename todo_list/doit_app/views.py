from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView, View, DeleteView
from .models import Task, Category, User
from .forms import AddTaskForm, UpdateTaskForm, SignUpForm, SelectMonthForm
from datetime import timedelta, datetime, date
import calendar
from todo_list.utils import Calendar
# Create your views here.


class TaskView(LoginRequiredMixin, DetailView):
    model = Task


class AddTaskView(LoginRequiredMixin, CreateView):
    template_name = 'doit_app/add-task.html'
    form_class = AddTaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name_suffix = '-update'
    success_url = reverse_lazy('task-list')

class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/task-list'



class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 30

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(user_id=self.request.user)


# Sign Up View
class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'doit_app/signup.html'

    def form_valid(self, form):
        if form.cleaned_data['password'] != form.cleaned_data['repeat_password']:
            form.add_error('password', 'Passwords are different')
            return super().form_invalid(form)
        User.objects.create_user(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'],
                                 email=form.cleaned_data['email'])
        return super().form_valid(form)


class MainPage(View):
    def get(self, request):
        return render(request, "doit_app/main-page.html")


class BudgetSummaryView(LoginRequiredMixin, View):
    def get(self, request):
        form = SelectMonthForm()
        return render(request, 'doit_app/budget-summary.html', context={"form": form})

    def post(self, request):
        form = SelectMonthForm(request.POST)
        tasks = list(Task.objects.filter (user_id=self.request.user))
        categories = list(Category.objects.all ())
        today = date.today ()
        this_year = today.year
        summary = []
        estimated_monthly_costs = 0
        final_monthly_costs = 0
        variance = 0
        if form.is_valid():
            chosen_month = int(form.cleaned_data['month'])
        for category in categories:
            summary.append({'category': category})
            for task in tasks:
                if task.start_time:
                    if task.start_time.month == chosen_month and task.start_time.year == this_year and task.category == category:
                        estimated_monthly_costs += float(task.estimated_cost)
                        final_monthly_costs += float(task.final_cost)
                        variance = estimated_monthly_costs - final_monthly_costs
            summary.append({'estimated': estimated_monthly_costs,
                            'final': final_monthly_costs,
                            'variance': variance})
            estimated_monthly_costs = 0
            final_monthly_costs = 0
            variance = 0
        ctx = {"summary": summary,
               "chosen_month": calendar.month_name[chosen_month]}

        return render(request, "doit_app/budget-summary.html", ctx)


class CompletionSummaryView(LoginRequiredMixin, View):
    def get(self, request) :
        form = SelectMonthForm ()
        return render(request, 'doit_app/completion-summary.html', context={"form": form})
    def post(self, request):
        form = SelectMonthForm (request.POST)
        today = date.today()
        this_year = today.year
        tasks = list(Task.objects.filter(user_id=self.request.user))
        number_of_tasks = 0
        number_of_tasks_completed = 0
        if form.is_valid () :
            chosen_month = int(form.cleaned_data['month'])
        for task in tasks:
            if task.start_time.month == chosen_month and task.start_time.year == this_year:
                number_of_tasks += 1
                if task.completed:
                    number_of_tasks_completed += 1

        if number_of_tasks == 0:
            ctx = {"no_task" : "Seems like you haven't added any tasks yet.",
                   "chosen_month": calendar.month_name[chosen_month]}
        else:
            number = float(number_of_tasks_completed/number_of_tasks)
            percentage = f"{number:.2%}"
            good_job_message = f"Congratulations! You have completed {percentage} of your tasks this month," \
                           f"great job!"
            if number >= 0.80:
                ctx = {"message": good_job_message,
                       "chosen_month": calendar.month_name[chosen_month]}
            else:
                ctx = {"summary": percentage,
                       "chosen_month": calendar.month_name[chosen_month]}

        return render(request, "doit_app/completion-summary.html", ctx)


