from rest_framework import serializers
from .models import Sprint, Task

class SprintSerializer(serializers.Serializer):

    class Meta: 
        model = Sprint
        fields = [
            'id',
            'name',
            'description',
            'end_date',
        ]

class TaskSerializers(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD
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