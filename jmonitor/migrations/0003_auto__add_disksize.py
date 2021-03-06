# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DiskSize'
        db.create_table(u'jmonitor_disksize', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('total', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('used', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cdt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'jmonitor', ['DiskSize'])


    def backwards(self, orm):
        # Deleting model 'DiskSize'
        db.delete_table(u'jmonitor_disksize')


    models = {
        u'jmonitor.disksize': {
            'Meta': {'object_name': 'DiskSize'},
            'cdt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'used': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'jmonitor.tcpconncount': {
            'Meta': {'object_name': 'TcpConnCount'},
            'cdt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'cnt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['jmonitor']