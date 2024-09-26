# Generated by Django 5.0.7 on 2024-09-26 02:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_comment_caso_alter_image_caso'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='desarrollador',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('groups__name__in', ['dev'])), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_dev', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comentario',
            field=models.TextField(blank=True, null=True),
        ),
    ]
