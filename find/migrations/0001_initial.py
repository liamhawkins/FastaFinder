# Generated by Django 2.2.6 on 2019-11-02 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_query', models.CharField(max_length=255)),
                ('sequence', models.TextField()),
                ('source', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_time_queried', models.DateTimeField(auto_now_add=True)),
                ('most_recent_time_queried', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_time_queried', models.DateTimeField(auto_now_add=True)),
                ('most_recent_time_queried', models.DateTimeField(auto_now=True)),
                ('raw_query', models.CharField(max_length=50)),
                ('fasta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='find.Fasta')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_queries', to='find.User')),
            ],
        ),
    ]
