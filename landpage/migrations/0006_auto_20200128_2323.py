# Generated by Django 2.2.2 on 2020-01-28 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0005_auto_20200128_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherstz',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacherstz',
            name='interest',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacherstz',
            name='position',
            field=models.TextField(blank=True, null=True),
        ),
    ]
