# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 11:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20161202_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=70)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='UserWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_remider', models.DateTimeField(auto_now=True)),
                ('following_remider', models.DateTimeField(null=True)),
                ('memory_lapses', models.PositiveIntegerField(default=0)),
                ('success_repetitions', models.PositiveIntegerField(default=0)),
                ('absolute_difficulty', models.PositiveIntegerField(default=0)),
                ('done', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='group',
        ),
        migrations.RemoveField(
            model_name='category',
            name='words',
        ),
        migrations.RemoveField(
            model_name='masteredword',
            name='user',
        ),
        migrations.RemoveField(
            model_name='masteredword',
            name='word',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mastered_words',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='difficulty',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['title', 'textbook_id']},
        ),
        migrations.AlterModelOptions(
            name='textbook',
            options={'ordering': ['title', 'owner_id']},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='wordclass',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='group',
            name='textbook',
        ),
        migrations.RemoveField(
            model_name='group',
            name='users',
        ),
        migrations.AddField(
            model_name='group',
            name='joined_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owned_groups', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='textbook',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='textbook',
            unique_together=set([('owner', 'title')]),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='MasteredWord',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.AddField(
            model_name='userword',
            name='adaptive_difficulty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Difficulty'),
        ),
        migrations.AddField(
            model_name='userword',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userword',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Word'),
        ),
        migrations.AddField(
            model_name='test',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Group'),
        ),
        migrations.AddField(
            model_name='test',
            name='textbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Textbook'),
        ),
        migrations.AddField(
            model_name='test',
            name='words',
            field=models.ManyToManyField(blank=True, to='api.Word'),
        ),
        migrations.AddField(
            model_name='word',
            name='users',
            field=models.ManyToManyField(blank=True, through='api.UserWord', to=settings.AUTH_USER_MODEL),
        ),
    ]
