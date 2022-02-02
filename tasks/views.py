from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

tasks = []
completed_tasks = []


def tasks_view(request):
    return render(request, "tasks.html", {"tasks": tasks})


def add_task_view(
    request,
):
    task_value = request.GET.get("task")
    tasks.append(task_value)
    return HttpResponseRedirect("/tasks/")


def delete_task_view(request, index):
    del tasks[index - 1]
    return HttpResponseRedirect("/tasks/")


def complete_task_view(request, index):
    completed_tasks.append(tasks[index - 1])
    del tasks[index - 1]
    print(completed_tasks)
    return HttpResponseRedirect("/completed_tasks/")


def completed_tasks_view(request):
    return render(request, "completed_tasks.html", {"completed_tasks": completed_tasks})


def all_tasks_view(request):
    return render(
        request, "all_tasks.html", {"tasks": tasks, "completed_tasks": completed_tasks}
    )
