# Generated by Django 5.0.7 on 2024-09-04 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='caso',
            field=models.ForeignKey(default=17, on_delete=django.db.models.deletion.CASCADE, to='core.caso'),
        ),
    ]
