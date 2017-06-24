# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-23 12:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csrfToken', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('coverPhoto', models.ImageField(upload_to=b'ebookShop/static/img')),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ebookShop.Author')),
            ],
        ),
        migrations.CreateModel(
            name='BookFactorDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('book', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ebookShop.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalCost', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='bookfactordetails',
            name='factor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ebookShop.Factor'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ebookShop.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='publication',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ebookShop.Publication'),
        ),
        migrations.AddField(
            model_name='basketitem',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ebookShop.Book'),
        ),
        migrations.AddField(
            model_name='basketitem',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
