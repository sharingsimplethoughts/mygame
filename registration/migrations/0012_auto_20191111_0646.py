# Generated by Django 2.2.5 on 2019-11-11 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_auto_20190930_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereduser',
            name='profile_image',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]