# Generated by Django 5.0.6 on 2024-06-29 12:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator('^\\d{9}$', 'Please enter exactly 9 digits.')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='Invalid email address.')])),
                ('phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Invalid Israeli phone number. Please enter 10 digits starting with 05 .', regex='^(05\\d|0[23489])\\d{7}$')])),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]