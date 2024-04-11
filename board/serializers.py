from rest_framework import serializers
from .models import Sprint, Task
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from datetime import date
from django.utils.translation import gettext_lazy as _

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
            'links',
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
                    ),
            'tasks':'{}?assigned={}'.format(
                            reverse(
                                'task-list',
                                request=request
                            ),
                            username
                        )
        }




class SprintSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField('get_links')
    class Meta: 
        model = Sprint
        fields = [
            'id',
            'name',
            'description',
            'end_date',
            'links',
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
                    ),
            'tasks': reverse(
                        'task-list',request=request
                    ) + '?sprint={}'.format(obj.pk),
        }
    
    def validate_end_date(self, attrs):
        end_date = attrs.get('end_date')
        new = not self.object
        changed = self.object and self.object.end_date != end_date
        if(new or changed) and (end_date<date.today()):
            msg = _('Invalid End Date.')
            raise serializers.ValidationError(msg) 
        return attrs

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
            'links',
        ]
    
    def get_status_display(self, obj):
        return obj.get_status_display()
    
    def get_links(self,obj):
        request = self.context['request']
        links = {
            'self': reverse(
                        'task-detail', kwargs={
                            'pk':obj.pk
                        }, request=request
                    ),
            'sprint':None,
            'assigned': None,
        }
        if obj.sprint_id:
            links['sprint'] = reverse(
                'sprint-detail', kwargs={'pk':obj.sprint_id}, request=request
            )
        if obj.assigned:
            links['assigned'] = reverse(
                'user-detail', kwargs={User.USERNAME_FIELD:obj.assigned}, request=request
            )
        return links
    
    