# Generated by Django 3.1.3 on 2020-12-11 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True, unique_for_date='publish', verbose_name='Slug'),
        ),
    ]
