# Generated by Django 2.2.6 on 2019-11-13 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0004_auto_20191113_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='num_queries',
        ),
    ]