# Generated by Django 2.2.6 on 2019-11-13 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0003_remove_query_most_recent_time_queried'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='first_time_queried',
            new_name='datetime',
        ),
    ]