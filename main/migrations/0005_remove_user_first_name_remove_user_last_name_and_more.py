# Generated by Django 5.1.2 on 2024-10-24 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_user_passport_user_passport_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='middle_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='passport_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='passport_series',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
