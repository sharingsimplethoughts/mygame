# Generated by Django 2.2.5 on 2019-09-19 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20190919_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereduser',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pl_level', to='registration.Level'),
        ),
    ]