# Generated by Django 2.2.2 on 2020-05-14 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0010_auto_20200203_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherstz',
            name='lang',
            field=models.CharField(default='rus', max_length=100),
        ),
        migrations.AddField(
            model_name='texttz',
            name='lang',
            field=models.CharField(default='rus', max_length=100),
        ),
    ]
