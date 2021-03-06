# Generated by Django 2.1.7 on 2019-03-25 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_productimage_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ('article',), 'verbose_name': 'Product image', 'verbose_name_plural': 'Product images'},
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='vector',
        ),
        migrations.AddField(
            model_name='productimage',
            name='is_vectorized',
            field=models.BooleanField(default=False, verbose_name='Is vectorized'),
        ),
    ]
