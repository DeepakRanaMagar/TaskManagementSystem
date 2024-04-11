from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions,filters
from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializers, UserSerializers
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()

class DefaultsMixin(object):
    authentication_class = [
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    ]
    permissions_class = (
        permissions.IsAuthenticated,
    )
    paginate_by =25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end_date')
    serializer_class = SprintSerializer
    search_fields = ('name',)
    ordering_fields = (
        'ends',
        'name',
    )

class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    search_fields = (
        ''
    )

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializers

