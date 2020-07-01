# Generated by Django 2.2.5 on 2020-04-30 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20191111_0646'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(blank=True, max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('req_type', models.CharField(choices=[('1', 'friend request'), ('2', 'game request'), ('3', 'join group request'), ('4', 'online status'), ('5', 'from admin')], default='1', max_length=50)),
                ('ref_id', models.CharField(default='', max_length=100)),
                ('status', models.CharField(choices=[('1', 'active'), ('2', 'inactive'), ('3', 'expired')], default='1', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='n_user', to='registration.RegisteredUser')),
            ],
        ),
        migrations.DeleteModel(
            name='UserFriendList',
        ),
    ]
