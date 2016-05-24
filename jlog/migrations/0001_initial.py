# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table(u'jlog_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('remote_ip', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('login_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('log_path', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('pid', self.gf('django.db.models.fields.IntegerField')()),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'jlog', ['Log'])

        # Adding model 'Alert'
        db.create_table(u'jlog_alert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('is_finished', self.gf('django.db.models.fields.BigIntegerField')(default=False)),
        ))
        db.send_create_signal(u'jlog', ['Alert'])

        # Adding model 'TtyLog'
        db.create_table(u'jlog_ttylog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jlog.Log'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('cmd', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'jlog', ['TtyLog'])

        # Adding model 'ExecLog'
        db.create_table(u'jlog_execlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('host', self.gf('django.db.models.fields.TextField')()),
            ('cmd', self.gf('django.db.models.fields.TextField')()),
            ('remote_ip', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('result', self.gf('django.db.models.fields.TextField')(default='')),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'jlog', ['ExecLog'])

        # Adding model 'FileLog'
        db.create_table(u'jlog_filelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('host', self.gf('django.db.models.fields.TextField')()),
            ('filename', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('remote_ip', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('result', self.gf('django.db.models.fields.TextField')(default='')),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'jlog', ['FileLog'])


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table(u'jlog_log')

        # Deleting model 'Alert'
        db.delete_table(u'jlog_alert')

        # Deleting model 'TtyLog'
        db.delete_table(u'jlog_ttylog')

        # Deleting model 'ExecLog'
        db.delete_table(u'jlog_execlog')

        # Deleting model 'FileLog'
        db.delete_table(u'jlog_filelog')


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
        u'jlog.ttylog': {
            'Meta': {'object_name': 'TtyLog'},
            'cmd': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jlog.Log']"})
        }
    }

    complete_apps = ['jlog']