from ast import Delete

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from tasks.models import Task


class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)


class UserLoginView(LoginView):
    template_name = "user_login.html"


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = "/user/login"


def session_storage_view(request):
    total_views = request.session.get("total_views", 0)
    request.session["total_views"] = total_views + 1
    return HttpResponse(f"total views: {total_views} {request.user.is_authenticated}")


class GenericTaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = "/tasks"


class GenericTaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"


class TaskCreateForm(ModelForm):
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 10:
            raise ValidationError("Data too small")
        return title.upper()

    class Meta:

        model = Task
        fields = ["title", "description", "completed"]


class GenericTaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_update.html"
    success_url = "/tasks"


class GenericTaskCreateView(CreateView):
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = "/tasks"

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class GenericTaskView(LoginRequiredMixin, ListView):
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 2

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(deleted=False, user=self.request.user).filter(
            completed=False
        )
        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks


def complete_task_view(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/completed_tasks/")


def completed_tasks_view(request):
    completed_tasks = Task.objects.filter(deleted=False).filter(completed=True)
    return render(request, "completed_tasks.html", {"completed_tasks": completed_tasks})


def all_tasks_view(request):
    tasks = Task.objects.filter(deleted=False).filter(completed=False)
    completed_tasks = Task.objects.filter(deleted=False).filter(completed=True)
    return render(
        request, "all_tasks.html", {"tasks": tasks, "completed_tasks": completed_tasks}
    )
