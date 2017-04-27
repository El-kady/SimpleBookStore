# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 19:05
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SimpleBookStore', '0008_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SimpleBookStore.Author')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SimpleBookStore.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SimpleBookStore.Category')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SimpleBookStore.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='authors',
            field=models.ManyToManyField(related_name='followed_by', through='SimpleBookStore.ProfileAuthor', to='SimpleBookStore.Author'),
        ),
        migrations.AddField(
            model_name='profile',
            name='categories',
            field=models.ManyToManyField(related_name='followed_by', through='SimpleBookStore.ProfileCategory', to='SimpleBookStore.Category'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
