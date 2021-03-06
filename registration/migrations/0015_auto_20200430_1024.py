# Generated by Django 2.2.5 on 2020-04-30 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_userfriendlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfriendlist',
            name='status',
            field=models.CharField(choices=[('1', 'waiting'), ('2', 'accepted'), ('3', 'declined')], default='1', max_length=50),
        ),
        migrations.AlterField(
            model_name='usernotification',
            name='req_type',
            field=models.CharField(choices=[('1', 'game request'), ('2', 'online status'), ('3', 'join group request'), ('4', 'friend request'), ('5', 'from admin')], default='1', max_length=50),
        ),
    ]
