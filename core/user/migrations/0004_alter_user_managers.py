# Generated by Django 5.0.6 on 2024-06-25 11:52

import django.contrib.auth.models
import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_follower_options'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('publisher', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
