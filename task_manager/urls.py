from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from tasks.views import *

from django.contrib.auth.views import LogoutView

from tasks.apiviews import TaskListAPI

from rest_framework.routers import SimpleRouter

from tasks.apiviews import TaskViewSet

router = SimpleRouter()

router.register("api/task", TaskViewSet)

urlpatterns = [
    path("taskapi/", TaskListAPI.as_view()),
    path("", GenericPendingTaskView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("tasks/", GenericPendingTaskView.as_view(), name="pending"),
    path("create-task/", GenericTaskCreateView.as_view(), name="create"),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view(), name="update"),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view(), name="detail"),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view(), name="delete"),
    path("completed_tasks/", GenericCompletedTaskView.as_view(), name="completed"),
    path("complete_task/<int:index>/", complete_task_view, name="complete"),
    path("all_tasks/", GenericAllTaskView.as_view(), name="all"),
    path("user/signup/", UserCreateView.as_view(), name="signup"),
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
    path("__reload__/", include("django_browser_reload.urls")),
] + router.urls
