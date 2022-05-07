import re

from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views import View
from django_filters.rest_framework import (
    CharFilter,
    ChoiceFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task, STATUS_CHOICES


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff")


class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "completed",
            "created_date",
            "deleted",
            "user",
            "priority",
            "status",
        ]


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListAPI(APIView):
    def get(self, request):
        tasks = Task.objects.filter(deleted=False)
        data = TaskSerializer(tasks, many=True).data

        return Response({"tasks": data})
