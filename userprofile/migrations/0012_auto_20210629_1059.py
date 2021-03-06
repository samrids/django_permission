# Generated by Django 3.2.4 on 2021-06-29 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_remove_profile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('H', 'ที่บ้าน'), ('W', 'ที่ทำงาน'), ('U', 'ไม่ระบุ')], default='U', max_length=1),
        ),
        migrations.AddField(
            model_name='address',
            name='is_deafult',
            field=models.BooleanField(default=False),
        ),
    ]
