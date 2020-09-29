# Generated by Django 2.2.13 on 2020-09-04 12:06
import re

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [
        ('tulius', '0001_initial'),
        ('tulius', '0002_auto_20200107_1601'),
        ('tulius', '0003_user_stories_author')
    ]

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('vk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('password', models.CharField(
                    max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(
                    blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(
                    default=False,
                    help_text='Designates that this user has all permissions '
                              'without explicitly assigning them.',
                    verbose_name='superuser status')),
                ('username', models.CharField(
                    help_text='Required. 30 characters or fewer. Letters, '
                              'numbers and @/./+/-/_ characters',
                    max_length=30, unique=True,
                    validators=[
                        django.core.validators.RegexValidator(
                            re.compile('^[\\w.@+-]+$'),
                            'Enter a valid username.', 'invalid')
                    ], verbose_name='username')),
                ('email', models.EmailField(
                    blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(
                    default=False,
                    help_text='Designates whether the user can log into this '
                              'admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(
                    default=True,
                    help_text='Designates whether this user should be treated '
                              'as active. Unselect this instead of deleting '
                              'accounts.',
                    verbose_name='active')),
                ('date_joined', models.DateTimeField(
                    default=django.utils.timezone.now,
                    verbose_name='date joined')),
                ('avatar', models.ImageField(
                    blank=True, null=True, upload_to='avatars')),
                ('rank', models.CharField(
                    blank=True, default='', max_length=255, null=True,
                    verbose_name='rank')),
                ('show_played_games', models.BooleanField(
                    default=True, verbose_name='show played games')),
                ('show_played_characters', models.BooleanField(
                    default=True, verbose_name='show played characters')),
                ('show_online_status', models.BooleanField(
                    default=True, verbose_name='show on-line status')),
                ('hide_trustmarks', models.BooleanField(
                    default=False, verbose_name='hide trustmarks')),
                ('signature', models.TextField(
                    blank=True, default='', max_length=400,
                    verbose_name='signature')),
                ('compact_text', models.BooleanField(
                    default=False, verbose_name='compact text')),
                ('icq', models.CharField(
                    blank=True, default='', max_length=12,
                    verbose_name='ICQ')),
                ('skype', models.CharField(
                    blank=True, default='', max_length=50,
                    verbose_name='skype')),
                ('sex', models.SmallIntegerField(
                    choices=[(0, 'Not defined'), (1, 'Male'), (2, 'Female')],
                    default=0, verbose_name='sex')),
                ('game_inline', models.SmallIntegerField(
                    choices=[(0, 'Current time'), (1, 'Messages count')],
                    default=0, verbose_name='Show in game')),
                ('animation_speed', models.PositiveIntegerField(
                    default=1000, verbose_name='Animation speed')),
                ('not_readed_messages', models.SmallIntegerField(
                    default=0, editable=False, verbose_name='Show in game')),
                ('last_read_pm_id', models.PositiveIntegerField(
                    default=0, editable=False)),
                ('groups', models.ManyToManyField(
                    blank=True,
                    help_text='The groups this user belongs to. A user will '
                              'get all permissions granted to each of their '
                              'groups.',
                    related_name='user_set', related_query_name='user',
                    to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    help_text='Specific permissions for this user.',
                    related_name='user_set', related_query_name='user',
                    to='auth.Permission', verbose_name='user permissions')),
                ('vk_profile', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    to='vk.VK_Profile')),
                ('stories_author', models.PositiveIntegerField(
                    default=0, editable=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]