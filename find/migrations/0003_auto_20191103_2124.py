# Generated by Django 2.2.6 on 2019-11-03 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0002_auto_20191102_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='fasta',
            name='description',
            field=models.CharField(default='temp', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fasta',
            name='accession',
            field=models.CharField(max_length=15),
        ),
    ]
