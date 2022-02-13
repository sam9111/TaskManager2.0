from django.contrib import admin
from django.urls import path, include
from tasks.views import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", GenericPendingTaskView.as_view()),
    path("create-task/", GenericTaskCreateView.as_view()),
    path("update-task/<pk>/", GenericTaskUpdateView.as_view()),
    path("detail-task/<pk>/", GenericTaskDetailView.as_view()),
    path("delete-task/<pk>/", GenericTaskDeleteView.as_view()),
    # path("complete_task/<int:index>/", complete_task_view),
    path("completed_tasks/", GenericCompletedTaskView.as_view()),
    path("all_tasks/", GenericAllTaskView.as_view()),
    # path("sessiontest", session_storage_view),
    path("user/signup/", UserCreateView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    path("user/logout/", LogoutView.as_view()),
    path("__reload__/", include("django_browser_reload.urls")),
]
