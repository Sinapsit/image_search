# Generated by Django 2.2.5 on 2019-09-22 13:30

import django.contrib.postgres.fields
from django.db import migrations, models
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningConfigHDF5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=utils.models.vector_path, verbose_name='File')),
                ('filename_list', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), default=None, null=True, size=None, verbose_name='Filename list')),
                ('article_list', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), default=None, null=True, size=None, verbose_name='Article list')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
