# Generated by Django 5.0.7 on 2024-09-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_caso_prioridad_alter_caso_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caso',
            name='tipo',
            field=models.CharField(choices=[('1', 'accesibilidad'), ('2', 'automatización'), ('3', 'compatibilidad'), ('4', 'funcional'), ('5', 'rendimiento'), ('6', 'seguridad'), ('7', 'usabilidad'), ('8', 'otro')], default=0, max_length=1),
        ),
    ]
