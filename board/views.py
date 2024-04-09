from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions
from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializers, UserSerializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end_date')
    serializer_class = SprintSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializers