# Generated by Django 5.0.6 on 2024-08-18 11:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=30, unique=True)),
                ('Password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator('^\\d{9}$', 'Please enter exactly 9 digits.')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('grade', models.CharField(choices=[('A', 'First grade'), ('B', 'Second grade'), ('C', 'Third grade'), ('D', 'Fourth grade'), ('E', 'Fifth grade'), ('F', 'Sixth grade')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('parent_name', models.CharField(max_length=100)),
                ('parent_phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Invalid Israeli phone number. Please enter 10 digits starting with 05.', regex='^(05\\d|0[23489])\\d{7}$')])),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Technology', 'Technology'), ('Mathematics', 'Mathematics'), ('History', 'History'), ('English', 'English'), ('Geography', 'Geography'), ('Literature', 'Literature'), ('Science', 'Science')], max_length=20)),
            ],
        ),
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
                ('classes', models.CharField(choices=[('A', 'First grade'), ('B', 'Second grade'), ('C', 'Third grade'), ('D', 'Fourth grade'), ('E', 'Fifth grade'), ('F', 'Sixth grade')], help_text='Select the grade the teacher can educate', max_length=1)),
                ('subject', models.ForeignKey(help_text='Select the subject the teacher can teach', on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='tsweb.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='tsweb.admin')),
                ('recipients', models.ManyToManyField(related_name='received_messages', to='tsweb.teacher')),
            ],
        ),
    ]
