# Generated by Django 2.0.4 on 2018-04-18 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeMail',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID')),
                ('sender', models.CharField(max_length=200)),
                ('recipient', models.CharField(max_length=200)),
                ('sender_mail', models.CharField(max_length=200)),
                ('recipient_mail', models.CharField(max_length=200)),
                ('headers', models.TextField()),
                ('body', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID')),
                (
                    'code_name',
                    models.CharField(
                        default='',
                        max_length=40,
                        unique=True,
                        verbose_name='code name')),
                (
                    'order',
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        verbose_name='order')),
                (
                    'name',
                    models.CharField(
                        blank=True,
                        default='',
                        max_length=100,
                        null=True,
                        verbose_name='name')),
                (
                    'description',
                    models.CharField(
                        blank=True,
                        default='',
                        max_length=250,
                        null=True,
                        verbose_name='description')),
                (
                    'header_template',
                    models.TextField(
                        blank=True,
                        default='',
                        verbose_name='header template')),
                (
                    'body_template',
                    models.TextField(
                        blank=True,
                        default='',
                        verbose_name='body template')),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID')),
                (
                    'enabled',
                    models.BooleanField(
                        default=True, verbose_name='enabled')),
                (
                    'notification',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='users',
                        to='events.Notification',
                        verbose_name='notification')),
            ],
            options={
                'verbose_name': 'user notification',
                'verbose_name_plural': 'user notifications',
            },
        ),
    ]
