# Generated by Django 3.1 on 2021-06-27 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_address_amphur_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='amphur',
            name='province',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userprofile.province'),
        ),
    ]
