# Generated by Django 3.1.1 on 2020-09-10 09:29

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_other', '0001_squashed_0005_migrate_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='data',
            field=models.JSONField(
                default=dict,
                encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
        migrations.DeleteModel(
            name='OnlineUser',
        ),
    ]