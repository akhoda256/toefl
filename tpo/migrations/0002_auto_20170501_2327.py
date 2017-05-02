# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-01 18:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listeningpartofwritingquestion',
            old_name='sQuestion',
            new_name='wQuestion',
        ),
        migrations.RemoveField(
            model_name='readingpartofwritingquestion',
            name='sQuestion',
        ),
        migrations.AddField(
            model_name='readingpartofwritingquestion',
            name='wQuestion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tpo.WritingQuestion'),
        ),
    ]