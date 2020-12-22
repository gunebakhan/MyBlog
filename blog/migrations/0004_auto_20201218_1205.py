# Generated by Django 3.1.3 on 2020-12-18 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201212_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', related_query_name='replies', to='blog.comment', verbose_name='Relpy'),
        ),
    ]
