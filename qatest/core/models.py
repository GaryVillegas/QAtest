from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ValidationError

# Create your models here.
class Project(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    responsible_user = models.ForeignKey(User, related_name='assigned_project', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'analista'})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.responsible_user and self.responsible_user.assigned_project.count() >= 5:
            raise ValidationError("Un usuario no puede ser responsable de más de 5 proyectos.")
        super().save(*args, **kwargs)
    
class Caso(models.Model):
    tipo_caso = [
        ('1','accesibilidad'), ('2', 'automatización'), ('3', 'compatibilidad'),
        ('4', 'funcional'), ('5', 'rendimiento'), ('6', 'seguridad'), ('7', 'usabilidad'),
        ('8', 'otro')
    ]

    estado_caso = [
        ('1', 'Sin Ejecutar'),
        ('2', 'Aprobado'),
        ('3', 'Bloqueado'),
        ('4', 'Retesteado'),
        ('5', 'Fallido'),
    ]

    prioridad_caso = [
        ('1', 'bajo'), ('2', 'medio'), ('3', 'alto'), ('4', 'critico')
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, limit_choices_to=Q(groups__name__in=['analista', 'dev']), null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=tipo_caso, default=1)
    estado = models.CharField(max_length=1, choices=estado_caso, default=1)
    prioridad = models.CharField(max_length=1, choices=prioridad_caso, default=1)
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
    
    @property
    def estado_display(self):
        return dict(self.estado_caso).get(self.estado, 'Desconocido')

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comentario

class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
    
class Document(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    documento = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.documento.name
