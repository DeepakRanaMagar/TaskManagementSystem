from django.shortcuts import render
from rest_framework import viewsets
from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializers, UserSerializers
from django.contrib.auth import get_user_model
User = get_user_model()

class SprintViewset(viewsets.ModelViewSet):

    '''
        API Endpoints for Sprint
    '''
    queryset = Sprint.objects.order_by('end_date')
    serializer_class = SprintSerializer

class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):