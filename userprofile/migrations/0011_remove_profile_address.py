# Generated by Django 3.2.4 on 2021-06-28 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0010_profile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
    ]
