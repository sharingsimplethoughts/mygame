# Generated by Django 2.2.5 on 2019-09-19 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_auto_20190919_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereduser',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_level', to='registration.Level'),
        ),
    ]
