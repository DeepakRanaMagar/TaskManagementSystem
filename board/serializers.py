from rest_framework import serializers
from .models import Sprint, Task
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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
    
    def validate_end_date(self,value):
        '''
            Validate the Sprint End_date
        '''
        if value < date.today():
            raise ValidationError("Invalid Date Field")
        return value    


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
    
    def validate_sprint(self, value):
        if self.instance and self.instance.pk:
            if value != self.instance.sprint:
                if self.instance.status == Task.STATUS_DONE:
                    msg = _('Cannot change the sprint of a completed task.')
                    raise serializers.ValidationError(msg)
                if value and value.end < date.today():
                    msg = _('Cannot assign tasks to past sprints.')
                    raise serializers.ValidationError(msg)
        else:
            if value and value.end < date.today():
                msg = _('Cannot add tasks to past sprints.')
                raise serializers.ValidationError(msg)
        return value
            
    def validate(self, attrs):
        sprint = attrs.get('sprint')
        status = attrs.get('status', Task.STATUS_TODO)
        started = attrs.get('started')
        completed = attrs.get('completed')
        if not sprint and status != Task.STATUS_TODO:
            msg = _('Backlog tasks must have "Not Started" status.')
            raise serializers.ValidationError(msg)
        if started and status == Task.STATUS_TODO:
            msg = _('Started date cannot be set for not started tasks.')
            raise serializers.ValidationError(msg)
        if completed and status != Task.STATUS_DONE:
            msg = _('Completed date cannot be set for uncompleted tasks.')
            raise serializers.ValidationError(msg)
        return attrs
