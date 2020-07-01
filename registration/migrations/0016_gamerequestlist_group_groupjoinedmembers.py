# Generated by Django 2.2.5 on 2020-04-30 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0015_auto_20200430_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_players', models.PositiveIntegerField(default=2)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gr_ruser', to='registration.RegisteredUser')),
            ],
        ),
        migrations.CreateModel(
            name='GroupJoinedMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gm_group', to='registration.Group')),
                ('ruser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gm_ruser', to='registration.RegisteredUser')),
            ],
        ),
        migrations.CreateModel(
            name='GameRequestList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'waiting'), ('2', 'accepted'), ('3', 'declined')], default='1', max_length=50)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gr_friend', to='registration.RegisteredUser')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gr_user', to='registration.RegisteredUser')),
            ],
        ),
    ]
