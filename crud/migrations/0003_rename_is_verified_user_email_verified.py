# Generated by Django 5.0.1 on 2024-01-16 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_user_is_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_verified',
            new_name='email_verified',
        ),
    ]
