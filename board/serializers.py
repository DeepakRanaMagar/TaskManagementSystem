from rest_framework import serializers
from .models import Sprint, Task
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()

class UserSerializers(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source='get_full_name',
        read_only = True
    )
    links = serializers.SerializerMethodField('get_links')
    
    class Meta:
        model = User
        fields = (
            'id',
            User.USERNAME_FIELD,
            'full_name',
            'is_active',
        )
    
    def get_links(self,obj):
        request = self.context['request']
        username = obj.get_username()
        return {
            'self': reverse(
                'user-detail',
                kwargs = {
                    User.USERNAME_FIELD: username
                },
            request = request
            )
        }




class SprintSerializer(serializers.Serializer):
    links = serializers.SerializerMethodField('get_links')
    
    class Meta: 
        model = Sprint
        fields = [
            'id',
            'name',
            'description',
            'end_date',
        ]
    
    def get_links(self,obj):
        request = self.context['request']
        return {
            'self': reverse(
                'sprint-detail',
                kwargs = {
                    'pk': obj.pk
                },
            request = request
            )
        }
        


class TaskSerializers(serializers.ModelSerializer):
    links = serializers.SerializerMethodField('get_links')

    assigned = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD,
        queryset=User.objects.all(),
    )
    status_display = serializers.SerializerMethodField('get_status_display')
    
    class Meta: 
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'sprint',
            'status',
            'status_display',
            'assigned',
            'order',
            'start_date',
            'due_date',
            'completed_date',
        ]
    
    def get_status_display(self, obj):
        return obj.get_status_display()
    
    def get_links(self,obj):
        request = self.context['request']
        return {
            'self': reverse(
                'tasks-detail',
                kwargs = {
                    'pk': obj.pk
                },
            request = request
            )
        }