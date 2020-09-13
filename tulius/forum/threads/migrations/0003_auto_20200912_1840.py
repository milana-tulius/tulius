# Generated by Django 3.1.1 on 2020-09-12 15:40

import gc

from django.db import migrations, transaction

from tulius.forum.threads import models
from tulius.forum.threads import mutations
from tulius.forum.rights import mutations as rights_mutations
from tulius.forum.comments import mutations as comments_mutations

comments_mutations.init()


class Tmp(rights_mutations.UpdateRights):
    # to make usage of rights for linters
    pass


def migrate_data(apps, schema_editor):
    count = 0
    total_count = models.Thread.objects.filter(parent=None).count()
    for thread in models.Thread.objects.filter(parent=None).iterator(
            chunk_size=1000):
        with transaction.atomic():
            mutations.ThreadFixCounters(thread).apply()
        count += 1
        if count % 10 == 0:
            gc.collect()
            print(f'migrated {count} threads')
    print(f'Threads migrated {count} of {total_count}')


class Migration(migrations.Migration):

    dependencies = [
        ('forum_threads', '0002_auto_20200910_1212'),
    ]

    operations = [
        migrations.RunPython(migrate_data)
    ]
