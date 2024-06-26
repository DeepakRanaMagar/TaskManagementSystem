import django_filters
from .models import Task, Sprint
from django.contrib.auth import get_user_model

User = get_user_model()

class NullFilter(django_filters.BooleanFilter):

    def filter(self, qs, value):
        if value is not None:
            return qs.filter(
                **{'%s__isnull' %self.name:value}
            )   
        return qs

class TaskFilter(django_filters.FilterSet):
    backlog = NullFilter(name='sprint')
    
    class Meta:
        model = Task
        fields = (
            'sprint',
            'assigned',
            'status',
            'backlog',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['assigned'].extra.update(
            {'to_field_name':User.USERNAME_FIELD}
        )

class SprintFilter(django_filters.FilterSet):
    end_date_min = django_filters.DateFilter(name='end_date', lookup_type='gte')
    end_date_max = django_filters.DateFilter(name='end_date', lookup_type='lte')

    class Meta: 
        model = Sprint
        fields = (
            'end_date_min',
            'end_date_max',
        )