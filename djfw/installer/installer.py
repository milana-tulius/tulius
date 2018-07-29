def clear():
    from .models import BackupCategory
    obj_count = 0
    for category in BackupCategory.objects.all():
        obj_count += category.clear_backups()
    return obj_count
