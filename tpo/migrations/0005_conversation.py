# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-25 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tpo', '0004_auto_20170425_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('convNumber', models.IntegerField(default=1)),
                ('imgFile', models.FileField(upload_to='tpo/static/images/')),
                ('audioFile', models.FileField(upload_to='tpo/static/audio/')),
                ('tpo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpo.TPO')),
            ],
        ),
    ]
