# Generated by Django 2.2.13 on 2020-09-04 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ('gameforum', '0001_initial'),
        ('gameforum', '0002_auto_20200725_1124')
    ]

    initial = True

    dependencies = [
        ('game_forum_threads', '0001_squashed_0007_rights_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0001_squashed_0002_auto_20180418_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trustmark',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('value', models.SmallIntegerField(verbose_name='value')),
                ('role', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='trust_marks', to='stories.Role',
                    verbose_name='role')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='trust_marks', to=settings.AUTH_USER_MODEL,
                    verbose_name='user')),
                ('variation', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='trust_marks', to='stories.Variation',
                    verbose_name='variation')),
            ],
            options={
                'verbose_name': 'trust mark',
                'verbose_name_plural': 'trust marks',
                'unique_together': {('variation', 'user', 'role')},
            },
        ),
        migrations.CreateModel(
            name='GameThreadRight',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('access_level', models.SmallIntegerField(
                    choices=[
                        (3, 'read and write rights'), (1, 'read right'),
                        (7, 'read, write and moderate'),
                        (2, 'write only right'),
                        (5, 'read and moderate right(no write)')
                    ], default=3, verbose_name='access rights')),
                ('role', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='accessed_threads', to='stories.Role',
                    verbose_name='role')),
                ('thread', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='access_roles',
                    to='game_forum_threads.Thread', verbose_name='thread')),
            ],
            options={
                'verbose_name': 'game thread right',
                'verbose_name_plural': 'game thread rights',
                'unique_together': {('thread', 'role')},
            },
        ),
    ]
