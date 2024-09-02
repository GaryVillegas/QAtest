# Generated by Django 5.1 on 2024-09-02 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_case_caso'),
    ]

    operations = [
        migrations.CreateModel(
            name='CasoContenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precondicion', models.TextField(max_length=250)),
                ('pasos', models.TextField(max_length=250)),
                ('resultados_esperados', models.TextField(max_length=250)),
                ('caso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.caso')),
            ],
        ),
    ]
