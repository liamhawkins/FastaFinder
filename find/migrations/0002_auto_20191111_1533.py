# Generated by Django 2.2.6 on 2019-11-11 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='fasta',
            new_name='fasta_source',
        ),
    ]