# Generated by Django 2.0.4 on 2018-04-18 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID')),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name='updated at')),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='created at')),
                (
                    'position',
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name='Position')),
                (
                    'caption',
                    models.CharField(
                        default='', max_length=300, verbose_name='caption')),
                (
                    'announcement',
                    models.TextField(
                        blank=True,
                        default='',
                        null=True,
                        verbose_name='announcement')),
                (
                    'full_text',
                    models.TextField(
                        blank=True,
                        default='',
                        null=True,
                        verbose_name='full text')),
                (
                    'is_published',
                    models.BooleanField(
                        default=False, verbose_name='is published')),
                (
                    'published_at',
                    models.DateTimeField(verbose_name='published at')),
                (
                    'language',
                    models.CharField(
                        editable=False,
                        max_length=10,
                        verbose_name='language')),
            ],
            options={
                'verbose_name': 'news item',
                'verbose_name_plural': 'news items',
                'ordering': ['-published_at'],
                'abstract': False,
            },
        ),
    ]
