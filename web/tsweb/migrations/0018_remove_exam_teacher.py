# Generated by Django 5.0.6 on 2024-08-17 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsweb', '0017_exam_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='teacher',
        ),
    ]