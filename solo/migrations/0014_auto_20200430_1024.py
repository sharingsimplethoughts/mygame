# Generated by Django 2.2.5 on 2020-04-30 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solo', '0013_auto_20191120_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupjoinedmembers',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupjoinedmembers',
            name='ruser',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='GroupJoinedMembers',
        ),
    ]
