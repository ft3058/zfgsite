# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InterfaceIo'
        db.create_table(u'jmonitor_interfaceio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('insize', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('outsize', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('cdt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'jmonitor', ['InterfaceIo'])


    def backwards(self, orm):
        # Deleting model 'InterfaceIo'
        db.delete_table(u'jmonitor_interfaceio')


    models = {
        u'jmonitor.disksize': {
            'Meta': {'object_name': 'DiskSize'},
            'cdt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'used': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'jmonitor.interfaceio': {
            'Meta': {'object_name': 'InterfaceIo'},
            'cdt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insize': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'outsize': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
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