# Generated by Django 5.0.6 on 2024-08-20 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsweb', '0002_exam_question_subjectclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('numeric_grade', models.FloatField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsweb.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsweb.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_answer', models.CharField(max_length=1)),
                ('is_correct', models.BooleanField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsweb.exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsweb.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsweb.student')),
            ],
        ),
    ]
