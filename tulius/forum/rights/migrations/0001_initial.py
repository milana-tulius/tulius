# Generated by Django 2.2.13 on 2020-07-23 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum_threads', '0002_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadAccessRight',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('access_level', models.SmallIntegerField(
                    choices=[
                        (3, 'read and write rights'), (1, 'read right'),
                        (7, 'read, write and moderate'),
                        (2, 'write only right'),
                        (5, 'read and moderate right(no write)')],
                    default=3, verbose_name='access rights')),
                ('thread', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='granted_rights', to='forum_threads.Thread',
                    verbose_name='thread')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='forum_threads_rights',
                    to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'thread access right',
                'verbose_name_plural': 'threads access rights',
                'unique_together': {('thread', 'user')},
            },
        ),
    ]