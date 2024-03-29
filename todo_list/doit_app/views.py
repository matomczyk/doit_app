from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView, View, DeleteView
from .models import Task, Category, User, BudgetSummary, Subtask, TaskTag
from .forms import AddTaskForm, UpdateTaskForm, SignUpForm, SelectMonthForm, AddReminderForm, AddTagForm, AddSubtaskForm, \
                    UpdateSubtaskForm
from datetime import date
import calendar

# Create your views here.


class TaskView(LoginRequiredMixin, DetailView):
    """
    A view that allows user to see details of each task.
    A view also shows list of tags added to the task.
    """
    model = Task
    context_object_name = 'task'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        task = self.object
        context['tags'] = task.tasktag_set.values_list('name', flat=True)
        return context





class AddTaskView(LoginRequiredMixin, CreateView):
    """
    A view that allows user to add new task.
    """
    template_name = 'doit_app/add-task.html'
    form_class = AddTaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class UpdateTaskView(LoginRequiredMixin, UpdateView):
    """
    A view that has fields not used in AddTaskView, used to update task with completion check, final cost and end time.
    """
    model = Task
    form_class = UpdateTaskForm
    template_name_suffix = '-update'
    success_url = reverse_lazy('task-list')

class DeleteTaskView(LoginRequiredMixin, DeleteView):
    """
    A view that allows user to delete task.
    """
    model = Task
    success_url = '/task-list'



class TaskListView(LoginRequiredMixin, ListView):
    """
    A view that shows user all task created by them.
    """
    model = Task
    paginate_by = 30

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(user_id=self.request.user)


# Sign Up View
class SignUpView(FormView):
    """
    A view to create account.
    """
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
    """
    Welcome page view.
    """
    def get(self, request):
        return render(request, "doit_app/main-page.html")


class BudgetSummaryView(LoginRequiredMixin, View):
    """
    A view that allows user to see summarised monthly spending.
    There is a month selection field and spendings are divided by categories included in Category model.
    """
    def get(self, request):
        form = SelectMonthForm()
        return render(request, 'doit_app/budget-summary.html', context={"form": form})

    def post(self, request):
        form = SelectMonthForm(request.POST)
        tasks = list(Task.objects.filter (user_id=self.request.user))
        categories = list(Category.objects.all())
        today = date.today ()
        this_year = today.year
        summary = []
        estimated_monthly_costs = 0
        final_monthly_costs = 0
        variance = 0
        total_est = 0
        total = 0
        if form.is_valid():
            chosen_month = int(form.cleaned_data['month'])
        for category in categories:
            for task in tasks:
                if task.start_time:
                    if task.start_time.month == chosen_month and task.start_time.year == this_year and task.category == category:
                        estimated_monthly_costs += float(task.estimated_cost)
                        final_monthly_costs += float(task.final_cost)
                        variance = estimated_monthly_costs - final_monthly_costs
                        total_est += float(task.estimated_cost)
                        total += float(task.final_cost)
            summary.append({'estimated': estimated_monthly_costs,
                            'final': final_monthly_costs,
                            'variance': variance,
                            'category': category})
            estimated_monthly_costs = 0
            final_monthly_costs = 0
            variance = 0
            budget_summary = BudgetSummary.objects.create(month=calendar.month_name[chosen_month], total_cost=total)
        ctx = {"summary": summary,
               "chosen_month": calendar.month_name[chosen_month],
               "total": budget_summary}

        return render(request, "doit_app/budget-summary.html", ctx)


class CompletionSummaryView(LoginRequiredMixin, View):
    """
    A view that shows user percentage of completed tasks for chosen month.
    """
    def get(self, request):
        form = SelectMonthForm()
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



class AddTaskTag(LoginRequiredMixin, FormView):
    """
    A view that allows user to add custom tags to each task.
    """
    form_class = AddTagForm
    template_name = 'doit_app/add-tag.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        tag = self.request.POST.get("name")
        task_id = self.kwargs['pk']
        tag, _ = TaskTag.objects.get_or_create(name=tag)
        tag.task.add(task_id)
        return super().form_valid(form)
        

class AddSubtaskView(LoginRequiredMixin, View):
    """
    A view that allows user to add subtask to each task.
    """
    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        form = AddSubtaskForm()
        return render(request, 'doit_app/add-subtask.html', {'form': form, 'task': task})

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        form = AddSubtaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subtask = Subtask(task=task, name=name)
            subtask.save()
            return redirect('task-details', pk=pk)
        return render(request, 'doit_app/add-subtask.html', {'form': form, 'task': task})


class UpdateSubtaskView(LoginRequiredMixin, UpdateView):
    """
    A view that allows user to check completion box of subtasks.
    """
    model = Subtask
    form_class = UpdateSubtaskForm
    template_name_suffix = '-update'
    success_url = reverse_lazy('task-list')

class DeleteSubtaskView(LoginRequiredMixin, DeleteView):
    """
    A view that allows user to delete subtasks.
    """
    model = Subtask
    success_url = '/task-list'


class TaskSubtasksView(LoginRequiredMixin, View):
    """
    A view that shows list of subtasks for each task.
    """
    def get(self, request, pk) :
        task = Task.objects.get (id=pk)
        subtasks = task.subtask_set.all()
        return render(request, 'doit_app/task-subtasks.html', {'task': task, 'subtasks': subtasks})