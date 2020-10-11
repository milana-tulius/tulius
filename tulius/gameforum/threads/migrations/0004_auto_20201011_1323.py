# Generated by Django 3.1.1 on 2020-10-11 10:23

import gc

from django.db import migrations


def migrate_data(apps, schema_editor):
    count = 0
    thread_model = apps.get_model('game_forum_threads', 'Thread')
    for thread in thread_model.objects.filter(deleted=True).iterator(
            chunk_size=1000):
        if 'rights' not in thread.data:
            thread.data['rights'] = {
                'all': 0, 'su': 0, 'users': [], 'roles': [], 'all_roles': 0}
        thread.data['rights']['users'] = []
        thread.save()
        count += 1
        if count % 1000 == 0:
            gc.collect()
            print(f'migrated {count} threads')
    print(f'Threads migrated {count}')


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('game_forum_threads', '0003_auto_20200912_1854'),
    ]

    operations = [
        migrations.RunPython(migrate_data)
    ]
