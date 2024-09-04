from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Q

# Create your models here.
class Project(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    responsible_user = models.ForeignKey(User, related_name='assigned_project', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'analista'})

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

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField(null = True, blank = True)
    status = models.IntegerField(choices=status_name)
    priority = models.IntegerField(choices=priority_type)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responsible_user = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to=Q(groups__name__in=['analista', 'dev']))

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
class Caso(models.Model):
    tipo_caso = [
        ('1','accesibilidad'), ('2', 'automatización'), ('3', 'compatibilidad'),
        ('4', 'funcional'), ('5', 'rendimiento'), ('6', 'seguridad'), ('7', 'usabilidad'),
        ('8', 'otro')
    ]

    prioridad_caso = [
        ('1', 'bajo'), ('2', 'medio'), ('3', 'alto'), ('4', 'critico')
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to=Q(groups__name__in=['analista', 'dev']), null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tipo = models.IntegerField(choices=tipo_caso)
    prioridad = models.IntegerField(choices=prioridad_caso)
    estimado = models.TextField(max_length=10)
    precondicion = models.TextField(max_length=150, null=True, blank=True)
    pasos = models.TextField(max_length=150, null=True, blank=True)
    resultados_esperados = models.TextField(max_length=150, null=True, blank=True)

    @property
    def tipo_display(self):
        return dict(self.tipo_caso).get(self.tipo, 'Desconocido')
    
    @property
    def prioridad_display(self):
        return dict(self.prioridad_caso).get(self.prioridad, 'Desconocido')
    