# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RsyncCheckLog'
        db.create_table(u'jlog_rsyncchecklog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('host', self.gf('django.db.models.fields.TextField')(max_length=50, null=True)),
            ('cmd', self.gf('django.db.models.fields.TextField')(null=True)),
            ('remote_ip', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('result', self.gf('django.db.models.fields.TextField')(default='', null=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('check_status', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('file_num', self.gf('django.db.models.fields.TextField')(default='', null=True)),
            ('file_not_exists', self.gf('django.db.models.fields.TextField')(default='', null=True)),
            ('file_err_time', self.gf('django.db.models.fields.TextField')(default='', null=True)),
            ('file_err_size', self.gf('django.db.models.fields.TextField')(default='', null=True)),
            ('exec_seconds', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal(u'jlog', ['RsyncCheckLog'])


    def backwards(self, orm):
        # Deleting model 'RsyncCheckLog'
        db.delete_table(u'jlog_rsyncchecklog')


    models = {
        u'jlog.alert': {
            'Meta': {'object_name': 'Alert'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BigIntegerField', [], {'default': 'False'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'jlog.execlog': {
            'Meta': {'object_name': 'ExecLog'},
            'cmd': ('django.db.models.fields.TextField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'result': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'jlog.filelog': {
            'Meta': {'object_name': 'FileLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.TextField', [], {}),
            'host': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'result': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'jlog.log': {
            'Meta': {'object_name': 'Log'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'log_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'login_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pid': ('django.db.models.fields.IntegerField', [], {}),
            'remote_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'jlog.rsyncchecklog': {
            'Meta': {'object_name': 'RsyncCheckLog'},
            'check_status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'cmd': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'exec_seconds': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'file_err_size': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'file_err_time': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'file_not_exists': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'file_num': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'host': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'jlog.ttylog': {
            'Meta': {'object_name': 'TtyLog'},
            'cmd': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jlog.Log']"})
        }
    }

    complete_apps = ['jlog']