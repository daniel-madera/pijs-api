# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 01:05
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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=70)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Difficulty',
                'verbose_name_plural': 'Difficulties',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=70)),
                ('name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Group (Class)',
                'verbose_name_plural': 'Groups (Classes)',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, unique=True)),
                ('abbreviation', models.CharField(max_length=3, unique=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='MasteredWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_remider', models.DateTimeField(auto_now=True)),
                ('following_remider', models.DateTimeField(null=True)),
                ('memory_lapses', models.PositiveIntegerField(default=0)),
                ('success_repetitions', models.PositiveIntegerField(default=0)),
                ('absolute_difficulty', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Mastered word',
                'verbose_name_plural': 'Mastered words',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=70)),
            ],
            options={
                'ordering': ['title', 'textbook_id'],
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'App role',
                'verbose_name_plural': 'App roles',
            },
        ),
        migrations.CreateModel(
            name='Textbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=70)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Language')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textbooks', to='api.Profile')),
            ],
            options={
                'ordering': ['title', 'owner_id'],
                'verbose_name': 'Textbook',
                'verbose_name_plural': 'Textbooks',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=100)),
                ('meaning', models.CharField(max_length=100)),
                ('definition', models.CharField(blank=True, max_length=254, null=True)),
                ('definition_m', models.CharField(blank=True, max_length=254, null=True)),
                ('usage', models.CharField(blank=True, max_length=254, null=True)),
                ('usage_m', models.CharField(blank=True, max_length=254, null=True)),
                ('picture_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('thumbnail_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Difficulty')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='api.Module')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Word',
                'verbose_name_plural': 'Words',
            },
        ),
        migrations.CreateModel(
            name='WordClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Word class',
                'verbose_name_plural': 'Word classes',
            },
        ),
        migrations.AddField(
            model_name='word',
            name='word_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='words', to='api.WordClass'),
        ),
        migrations.AddField(
            model_name='profile',
            name='mastered_words',
            field=models.ManyToManyField(through='api.MasteredWord', to='api.Word'),
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Role'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='textbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='api.Textbook'),
        ),
        migrations.AddField(
            model_name='masteredword',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Profile'),
        ),
        migrations.AddField(
            model_name='masteredword',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Word'),
        ),
        migrations.AddField(
            model_name='group',
            name='textbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Textbook'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(to='api.Profile'),
        ),
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Group'),
        ),
        migrations.AddField(
            model_name='category',
            name='words',
            field=models.ManyToManyField(to='api.Word'),
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together=set([('value', 'module')]),
        ),
    ]