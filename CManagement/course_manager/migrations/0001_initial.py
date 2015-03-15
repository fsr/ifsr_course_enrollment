# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('current_count_of_participants', models.IntegerField(default=0)),
                ('weekday', models.CharField(max_length=10, default='Monday')),
                ('lesson', models.CharField(max_length=10, default='1.DS')),
                ('location', models.CharField(max_length=30)),
                ('attendance', models.IntegerField(default=15)),
                ('is_visible', models.BooleanField(default=True)),
                ('additional_information', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('is_visible', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseManagement',
            fields=[
                ('my_management', models.OneToOneField(serialize=False, to='course_manager.Management',
                                                       primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('user_ptr', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, auto_created=True,
                                                  parent_link=True, primary_key=True)),
                ('name_of_user', models.CharField(max_length=100)),
                ('s_number', models.CharField(max_length=200)),
                ('register_date', models.DateTimeField(verbose_name='registration date',
                                                       default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('useraccount_ptr', models.OneToOneField(serialize=False, to='course_manager.UserAccount',
                                                         auto_created=True, parent_link=True, primary_key=True)),
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('course_manager.useraccount',),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('useraccount_ptr', models.OneToOneField(serialize=False, to='course_manager.UserAccount',
                                                         auto_created=True, parent_link=True, primary_key=True)),
            ],
            options={
                'ordering': ('name_of_user',),
            },
            bases=('course_manager.useraccount',),
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('useraccount_ptr', models.OneToOneField(serialize=False, to='course_manager.UserAccount',
                                                         auto_created=True, parent_link=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('course_manager.useraccount',),
        ),
        migrations.CreateModel(
            name='UserManagement',
            fields=[
                ('my_management', models.OneToOneField(serialize=False, to='course_manager.Management',
                                                       primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tutor',
            name='the_management',
            field=models.ForeignKey(to='course_manager.Management'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizer',
            name='my_user_management',
            field=models.ForeignKey(to='course_manager.UserManagement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizer',
            name='the_management',
            field=models.ForeignKey(to='course_manager.Management'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='my_course_management',
            field=models.ForeignKey(to='course_manager.CourseManagement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='my_course',
            field=models.ForeignKey(to='course_manager.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='my_participants',
            field=models.ManyToManyField(to='course_manager.Participant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='my_tutor',
            field=models.ManyToManyField(to='course_manager.Tutor'),
            preserve_default=True,
        ),
    ]
