# Generated by Django 2.2.13 on 2020-09-04 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import tulius.forum.other.models


class Migration(migrations.Migration):

    replaces = [
        ('forum_other', '0001_initial'),
        ('forum_other', '0002_migration'),
        ('forum_other', '0003_auto_20200724_1032'),
        ('forum_other', '0004_commentlike_data'),
        ('forum_other', '0005_migrate_likes')
    ]

    initial = True

    dependencies = [
        ('forum_threads', '0001_squashed_0007_rights_migration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum_comments', '0001_squashed_0006_deleted_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadReadMark',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('not_readed_comment_id', models.IntegerField(
                    blank=True, db_index=True, null=True)),
                ('readed_comment_id', models.IntegerField()),
                ('thread', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='read_marks', to='forum_threads.Thread',
                    verbose_name='thread')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='forum_other_readed_threads',
                    to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'thread read mark',
                'verbose_name_plural': 'thread read marks',
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('comment', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='liked', to='forum_comments.Comment',
                    verbose_name='comment')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='liked_comments',
                    to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('data', jsonfield.fields.JSONField(
                    default=tulius.forum.other.models.default_json)),
            ],
            options={
                'verbose_name': 'comment like',
                'verbose_name_plural': 'comments likes',
            },
        ),
        migrations.CreateModel(
            name='VotingVote',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('choice', models.IntegerField(verbose_name='choice')),
                ('comment', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='votes', to='forum_comments.Comment',
                    verbose_name='comment')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='voting_votes', to=settings.AUTH_USER_MODEL,
                    verbose_name='user')),
            ],
            options={
                'verbose_name': 'voting vote',
                'verbose_name_plural': 'voting votes',
                'unique_together': {('user', 'comment')},
            },
        ),
        migrations.CreateModel(
            name='OnlineUser',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('visit_time', models.DateTimeField(
                    auto_now_add=True, verbose_name='visit time')),
                ('thread', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='visit_marks', to='forum_threads.Thread',
                    verbose_name='thread')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='forum_visit', to=settings.AUTH_USER_MODEL,
                    verbose_name='user')),
            ],
            options={
                'verbose_name': 'online user',
                'verbose_name_plural': 'online users',
                'unique_together': {('user', 'thread')},
            },
        ),
    ]
