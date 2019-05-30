# Generated by Django 2.1.3 on 2019-05-29 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('action_log_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('log_user', models.CharField(max_length=50)),
                ('log_detail', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'app_action_log',
                'ordering': ['action_log_id'],
            },
        ),
        migrations.CreateModel(
            name='ContainerInfoCache',
            fields=[
                ('container_info_cache_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=128)),
                ('host_port', models.IntegerField()),
                ('container_id', models.CharField(max_length=128)),
                ('image', models.CharField(max_length=128)),
                ('command', models.CharField(max_length=128)),
                ('created', models.CharField(max_length=128)),
                ('statename', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=128)),
                ('port', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('current_user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'app_container_info_cache',
                'ordering': ['container_info_cache_id'],
            },
        ),
        migrations.CreateModel(
            name='JobInfoCache',
            fields=[
                ('job_info_cache_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=128)),
                ('host_port_api', models.IntegerField()),
                ('host_protocal_api', models.CharField(max_length=128)),
                ('color', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('current_user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'app_job_info_cache',
                'ordering': ['job_info_cache_id'],
            },
        ),
        migrations.CreateModel(
            name='ProcessInfoCache',
            fields=[
                ('process_info_cache_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=128)),
                ('host_port', models.IntegerField()),
                ('statename', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('current_user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'app_process_info_cache',
                'ordering': ['process_info_cache_id'],
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('server_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=50)),
                ('port', models.IntegerField(default=0)),
                ('username', models.CharField(blank=True, default='', max_length=50)),
                ('password', models.CharField(blank=True, default='', max_length=256)),
                ('username_api', models.CharField(blank=True, default='', max_length=50)),
                ('password_api', models.CharField(blank=True, default='', max_length=256)),
                ('port_api', models.IntegerField(default=0)),
                ('protocal_api', models.CharField(blank=True, default='', max_length=50)),
                ('description', models.CharField(blank=True, default='', max_length=128)),
                ('server_type_id', models.IntegerField()),
            ],
            options={
                'db_table': 'app_server',
                'ordering': ['server_id'],
            },
        ),
        migrations.CreateModel(
            name='ServerInfoCache',
            fields=[
                ('server_info_cache_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('server_id', models.IntegerField()),
                ('host', models.CharField(max_length=50)),
                ('port', models.IntegerField()),
                ('port_api', models.IntegerField()),
                ('protocal_api', models.CharField(blank=True, default='', max_length=50)),
                ('description', models.CharField(blank=True, default='', max_length=128)),
                ('status', models.CharField(blank=True, default='', max_length=50)),
                ('server_type', models.CharField(max_length=50)),
                ('current_user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'app_server_info_cache',
                'ordering': ['server_info_cache_id'],
            },
        ),
        migrations.CreateModel(
            name='ServerType',
            fields=[
                ('server_type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('server_type', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'app_server_type',
                'ordering': ['server_type_id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email', models.CharField(blank=True, max_length=128)),
                ('role', models.CharField(blank=True, max_length=32)),
                ('description', models.CharField(blank=True, max_length=128)),
            ],
            options={
                'db_table': 'app_user',
                'ordering': ['user_id'],
            },
        ),
    ]
