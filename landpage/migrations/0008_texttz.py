# Generated by Django 2.2.2 on 2020-01-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0007_teacherstz_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextTZ',
            fields=[
                ('text_id', models.AutoField(primary_key=True, serialize=False)),
                ('text_name', models.CharField(max_length=100)),
                ('text', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
            ],
        ),
    ]
