# Generated by Django 2.0.4 on 2018-04-18 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='storyauthor',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='authored_stories',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='storyadmin',
            name='story',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='admins',
                to='stories.Story',
                verbose_name='story'),
        ),
        migrations.AddField(
            model_name='storyadmin',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='admined_stories',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='story',
            name='genres',
            field=models.ManyToManyField(
                blank=True,
                related_name='stories',
                to='stories.Genre',
                verbose_name='genres'),
        ),
        migrations.AddField(
            model_name='roledeletemark',
            name='role',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='delete_marks',
                to='stories.Role',
                verbose_name='role'),
        ),
        migrations.AddField(
            model_name='roledeletemark',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='role_delete_marks',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='role',
            name='avatar',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='roles',
                to='stories.Avatar',
                verbose_name='avatar'),
        ),
        migrations.AddField(
            model_name='role',
            name='character',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='roles',
                to='stories.Character',
                verbose_name='character'),
        ),
        migrations.AddField(
            model_name='role',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='roles',
                to=settings.AUTH_USER_MODEL,
                verbose_name='user'),
        ),
        migrations.AddField(
            model_name='role',
            name='variation',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='roles',
                to='stories.Variation',
                verbose_name='variation'),
        ),
        migrations.AddField(
            model_name='illustration',
            name='story',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='illustrations',
                to='stories.Story',
                verbose_name='story'),
        ),
        migrations.AddField(
            model_name='illustration',
            name='variation',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='illustrations',
                to='stories.Variation',
                verbose_name='variation'),
        ),
        migrations.AddField(
            model_name='character',
            name='avatar',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='characters',
                to='stories.Avatar',
                verbose_name='avatar'),
        ),
        migrations.AddField(
            model_name='character',
            name='story',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='characters',
                to='stories.Story',
                verbose_name='story'),
        ),
        migrations.AddField(
            model_name='avataralternative',
            name='avatar',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='alternatives',
                to='stories.Avatar',
                verbose_name='avatar'),
        ),
        migrations.AddField(
            model_name='avatar',
            name='story',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='avatars',
                to='stories.Story',
                verbose_name='story'),
        ),
        migrations.AddField(
            model_name='additionalmaterial',
            name='story',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='additional_materials',
                to='stories.Story',
                verbose_name='story'),
        ),
        migrations.AddField(
            model_name='additionalmaterial',
            name='variation',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='additional_materials',
                to='stories.Variation',
                verbose_name='variation'),
        ),
        migrations.AlterUniqueTogether(
            name='storyauthor',
            unique_together={('story', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='storyadmin',
            unique_together={('story', 'user')},
        ),
    ]
