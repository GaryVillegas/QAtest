# Generated by Django 5.0.7 on 2024-09-26 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_comment_desarrollador_alter_comment_comentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='desarrollador',
        ),
    ]
