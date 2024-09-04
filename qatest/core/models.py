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
    titulo = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=tipo_caso)
    prioridad = models.CharField(max_length=1, choices=prioridad_caso)
    estimado = models.CharField(max_length=10)
    precondicion = models.TextField(max_length=150, null=True, blank=True)
    pasos = models.TextField(max_length=150, null=True, blank=True)
    resultados_esperados = models.TextField(max_length=150, null=True, blank=True)

    @property
    def tipo_display(self):
        return dict(self.tipo_caso).get(self.tipo, 'Desconocido')
    
    @property
    def prioridad_display(self):
        return dict(self.prioridad_caso).get(self.prioridad, 'Desconocido')

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, default=17)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
