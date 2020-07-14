# Generated by Django 3.0.8 on 2020-07-14 16:51

import directory.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=directory.models.get_account_path)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=14)),
                ('room_no', models.CharField(max_length=100, verbose_name='Room No')),
                ('subjects', models.ManyToManyField(to='directory.Subject')),
            ],
        ),
    ]