# Generated by Django 2.2.13 on 2020-06-22 15:18

from django.db import migrations
import jsonfield.fields
import tulius.forum.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20200516_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='media',
            field=jsonfield.fields.JSONField(
                default=tulius.forum.models.default_media),
        ),
    ]
