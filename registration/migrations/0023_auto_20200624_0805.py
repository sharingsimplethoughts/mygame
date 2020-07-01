# Generated by Django 2.2.5 on 2020-06-24 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0022_registereduser_profile_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='type',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='l_name', to='registration.LevelType'),
        ),
    ]
