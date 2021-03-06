# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-08 04:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_student', models.CharField(max_length=100)),
                ('name_student', models.CharField(max_length=500)),
                ('note', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(default='', max_length=100)),
                ('terminal_objetive', models.CharField(max_length=500)),
                ('activity', models.CharField(max_length=500)),
                ('approved', models.CharField(default='', max_length=500)),
                ('notapproved', models.CharField(default='', max_length=500)),
                ('weight', models.PositiveIntegerField()),
                ('problem_id', models.IntegerField()),
                ('contest_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='evaluation',
            name='rubric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='professor.Rubric'),
        ),
    ]
