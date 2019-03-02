# Generated by Django 2.1 on 2019-03-01 11:02

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chaptername', models.TextField()),
                ('course_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseNames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=150, null=True)),
                ('teacher_id', models.IntegerField()),
                ('subscribeIds', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('opt_a', models.CharField(max_length=150)),
                ('opt_b', models.CharField(max_length=150)),
                ('opt_c', models.CharField(max_length=150)),
                ('opt_d', models.CharField(max_length=150)),
                ('answer', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_id', models.IntegerField()),
                ('chapter_id', models.IntegerField()),
                ('course_id', models.IntegerField(null=True)),
                ('quiz_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizParticipants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_id', models.IntegerField()),
                ('Quiz_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.TextField(blank=True, null=True)),
                ('role', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topicName', models.TextField()),
                ('chapter_id', models.IntegerField()),
                ('course_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='userProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.TextField(blank=True, max_length=100, null=True)),
                ('mobile_number', models.TextField(blank=True, null=True, unique=True)),
                ('role', models.TextField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
