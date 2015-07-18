# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ClientCollapse.modules'
        db.add_column(u'profiler_clientcollapse', 'modules',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ClientCollapse.modules'
        db.delete_column(u'profiler_clientcollapse', 'modules')


    models = {
        u'profiler.clientcollapse': {
            'Meta': {'object_name': 'ClientCollapse'},
            'browsers': ('django.db.models.fields.TextField', [], {}),
            'day': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'devices': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.TextField', [], {}),
            'oses': ('django.db.models.fields.TextField', [], {})
        },
        u'profiler.profilermessage': {
            'Meta': {'ordering': "['module_name', 'func_name', '-id']", 'object_name': 'ProfilerMessage'},
            'browser': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'browser_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'db_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'db_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'device': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exec_param': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exec_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'func_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'module_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'template_db_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'template_db_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'template_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'thread_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'profiler.timecollapse': {
            'Meta': {'object_name': 'TimeCollapse'},
            'anon_calls_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'calls_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'day': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'db_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'db_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'exceptions_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'exec_time': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobiles_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'template_db_count': ('django.db.models.fields.BigIntegerField', [], {}),
            'template_db_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'template_time': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['profiler']