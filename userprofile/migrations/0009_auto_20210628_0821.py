# Generated by Django 3.2.4 on 2021-06-28 01:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0008_auto_20210628_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amphures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('name_th', models.CharField(max_length=150)),
                ('name_en', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postcode', models.IntegerField()),
                ('name_th', models.CharField(max_length=150)),
                ('name_en', models.CharField(max_length=150)),
                ('amphure', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userprofile.amphures')),
            ],
        ),
        migrations.CreateModel(
            name='Geographies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2)),
                ('name_th', models.CharField(max_length=150)),
                ('name_en', models.CharField(max_length=150)),
                ('geography', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.geographies')),
            ],
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Amphur',
        ),
        migrations.DeleteModel(
            name='Province',
        ),
        migrations.AddField(
            model_name='amphures',
            name='province',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userprofile.provinces'),
        ),
        migrations.AddField(
            model_name='address',
            name='district',
            field=models.ForeignKey(default=100101, on_delete=django.db.models.deletion.CASCADE, to='userprofile.districts'),
        ),
    ]
