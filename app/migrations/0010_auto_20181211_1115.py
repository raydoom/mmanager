# Generated by Django 2.1.3 on 2018-12-11 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_jenkins_server_apiversion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='user_info',
            name='roles',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
