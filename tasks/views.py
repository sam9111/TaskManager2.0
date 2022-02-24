from ast import Delete

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from tasks.models import Task


class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(deleted=False, user=self.request.user).order_by(
            "priority", "-created_date"
        )
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks


# user signup
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return super(CreateView, self).get(request, *args, **kwargs)


# user login
class UserLoginView(LoginView):
    template_name = "user_login.html"
    redirect_authenticated_user = True


# list of tasks
class GenericAllTaskView(AuthorisedTaskManager, ListView):
    template_name = "all_tasks.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["completed_count"] = (
            super().get_queryset().filter(completed=True).count()
        )
        return context


class GenericCompletedTaskView(AuthorisedTaskManager, ListView):
    template_name = "completed_tasks.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(completed=True)


class GenericPendingTaskView(AuthorisedTaskManager, ListView):
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(completed=False)


# creating task
class TaskCreateForm(ModelForm):
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise ValidationError("Title too small!")
        return title.capitalize()

    class Meta:

        model = Task
        fields = ["title", "description", "priority", "completed"]


def check_priority(obj, update=False):
    priority = obj.priority
    tasks = Task.objects.filter(deleted=False, user=obj.user, completed=False)
    if update:
        tasks = tasks.exclude(id=obj.id)

    objs = []
    while task := tasks.filter(priority=priority).first():
        priority += 1
        task.priority = priority
        objs.append(task)

    Task.objects.bulk_update(objs, ["priority"])


class GenericTaskCreateView(AuthorisedTaskManager, CreateView):
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        check_priority(self.object)
        self.object.save()
        return HttpResponseRedirect(self.success_url)


# update a task
class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_update.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if "priority" in form.changed_data:
            check_priority(self.object, True)
        self.object.save()
        return HttpResponseRedirect(self.success_url)


# one task view
class GenericTaskDetailView(AuthorisedTaskManager, DetailView):
    model = Task
    template_name = "task_detail.html"


# delete a task
class GenericTaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy("home")


def complete_task_view(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect(reverse("completed"))
