from rest_framework.routers import DefaultRouter
from .views import SprintViewSet, TaskViewSet, UserViewSet
from django.urls import path

router = DefaultRouter()

router.register(r'sprints', SprintViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)

urlpatterns =[]+ router.urls
