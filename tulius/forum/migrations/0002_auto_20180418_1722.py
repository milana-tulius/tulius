# Generated by Django 2.0.4 on 2018-04-18 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='votingvote',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='voting_votes',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='votingchoice',
            name='voting',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='choices',
                to='forum.Voting',
                verbose_name='voting'),
        ),
        migrations.AddField(
            model_name='voting',
            name='comment',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='voting_list',
                to='forum.Comment',
                verbose_name='comment'),
        ),
        migrations.AddField(
            model_name='voting',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='create_votings',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='forum_files',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='threadreadmark',
            name='not_readed_comment',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='not_readed_users',
                to='forum.Comment',
                verbose_name='not readed comment'),
        ),
        migrations.AddField(
            model_name='threadreadmark',
            name='readed_comment',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='readed_users',
                to='forum.Comment',
                verbose_name='readed comment'),
        ),
        migrations.AddField(
            model_name='threadreadmark',
            name='thread',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='read_marks',
                to='forum.Thread',
                verbose_name='thread'),
        ),
        migrations.AddField(
            model_name='threadreadmark',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='forum_readed_threads',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='threaddeletemark',
            name='thread',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='delete_marks',
                to='forum.Thread',
                verbose_name='thread'),
        ),
        migrations.AddField(
            model_name='threaddeletemark',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='thread_delete_marks',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='threadcollapsestatus',
            name='thread',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='forum.Thread',
                verbose_name='thread'),
        ),
        migrations.AddField(
            model_name='threadcollapsestatus',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='threadaccessright',
            name='thread',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='rights',
                to='forum.Thread',
                verbose_name='thread'),
        ),
        migrations.AddField(
            model_name='threadaccessright',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='forum_theads_rights',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='thread',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='children',
                to='forum.Thread',
                verbose_name='parent thread'),
        ),
        migrations.AddField(
            model_name='thread',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='forum_threads',
                to=settings.AUTH_USER_MODEL,
                verbose_name='author'),
        ),
        migrations.AddField(
            model_name='onlineuser',
            name='thread',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='visit_marks',
                to='forum.Thread',
                verbose_name='thread'),
        ),
        migrations.AddField(
            model_name='onlineuser',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='forum_visit',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='liked',
                to='forum.Comment',
                verbose_name='comment'),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='liked_comments',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='commentdeletemark',
            name='comment',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='delete_marks',
                to='forum.Comment',
                verbose_name='comment'),
        ),
        migrations.AddField(
            model_name='commentdeletemark',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='comments_delete_marks',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='editor',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='forum_comments_edited',
                to=settings.AUTH_USER_MODEL,
                verbose_name='edited by'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='comments',
                to='forum.Thread',
                verbose_name='thread'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='answers',
                to='forum.Comment',
                verbose_name='reply to'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='forum_comments',
                to=settings.AUTH_USER_MODEL,
                verbose_name='author'),
        ),
        migrations.AlterUniqueTogether(
            name='votingvote',
            unique_together={('choice', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='threadcollapsestatus',
            unique_together={('thread', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='threadaccessright',
            unique_together={('thread', 'user')},
        ),
    ]
