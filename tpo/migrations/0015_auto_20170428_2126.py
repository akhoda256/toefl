# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-28 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0014_speakingquestion_responsetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='speakingresponse',
            name='questionNo',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='speakingresponse',
            name='tpoNo',
            field=models.IntegerField(default=1),
        ),
    ]
