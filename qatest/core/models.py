from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    status_name=[
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Testing'),
        (4, 'Done')
    ]

    priority_type=[
        (1, '1'), (2, '2'), (3, '3'), (4, '4')
    ]

    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField(null = True, blank = True)
    status = models.IntegerField(choices=status_name)
    priority = models.IntegerField(choices=priority_type)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responsible_user = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name