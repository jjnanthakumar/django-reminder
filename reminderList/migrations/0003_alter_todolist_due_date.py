# Generated by Django 4.0.5 on 2022-06-26 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminderList', '0002_remove_todolist_status_todolist_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 20, 24, 18, 586392)),
        ),
    ]
