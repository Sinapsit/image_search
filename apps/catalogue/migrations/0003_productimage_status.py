# Generated by Django 2.1.7 on 2019-03-24 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20190323_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Not loaded'), (1, 'Loaded'), (3, 'Not found')], default=0),
        ),
    ]
