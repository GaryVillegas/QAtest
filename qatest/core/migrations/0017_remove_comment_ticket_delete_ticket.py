# Generated by Django 5.0.7 on 2024-09-04 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_title_caso_titulo_alter_caso_prioridad_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='ticket',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]