# Generated by Django 5.0.7 on 2024-08-14 17:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'To Do'), (2, 'In Progress'), (3, 'Testing'), (4, 'Done')])),
                ('priority', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
                ('responsible_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
