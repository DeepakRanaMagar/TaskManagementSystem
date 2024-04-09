from django.db import models
from django.utils.translation import ugettext_lazy as _

class Sprint(models.Model):
    name = models.CharField(max_length=50, null=True, default='')
    description = models.TextField(max_length=150, null=True, default='')
    end_date = models.DateTimeField(unique=True)

    def __str__(self):
        return self.name or _('Sprint Ending %s')%self.end_date

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=150, default='', null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)


    STATUS_TODO = 1
    STATUS_IN_PROGRESS =2 
    STATUS_TESTING = 3
    STATUS_DONE = 4

    STATUS_CHOICES = (
        (STATUS_TODO, _('Not Started')),
        (STATUS_IN_PROGRESS, _('WORKING ON')),
        (STATUS_TESTING, _('TESTING')),
        (STATUS_DONE, _('FINISHED')),
    )

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default='STATUS_TODO')
    