from django.shortcuts import render
from rest_framework import viewsets
from .models import Sprint, Task
from .serializers import SprintSerializer

class SprintViewset(viewsets.ModelViewSet):

    '''
        API Endpoints for Sprint
    '''
    queryset = Sprint.objects.order_by('end_date')
    serializer_class = SprintSerializer