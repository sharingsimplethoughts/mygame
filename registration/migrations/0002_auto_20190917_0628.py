# Generated by Django 2.2.5 on 2019-09-17 06:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereduser',
            name='inactive_from',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='registereduser',
            name='is_engaged',
            field=models.BooleanField(default=False),
        ),
    ]
