# Generated by Django 5.1.1 on 2024-09-20 22:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_alter_document_documento_alter_image_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='responsible_user',
        ),
        migrations.AddField(
            model_name='project',
            name='responsible_user',
            field=models.ManyToManyField(blank=True, limit_choices_to={'groups__name': 'analista'}, related_name='assigned_project', to=settings.AUTH_USER_MODEL),
        ),
    ]
