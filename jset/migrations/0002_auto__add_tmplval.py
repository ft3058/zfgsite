# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TmplVal'
        db.create_table(u'jset_tmplval', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cdt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('udt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'jset', ['TmplVal'])


    def backwards(self, orm):
        # Deleting model 'TmplVal'
        db.delete_table(u'jset_tmplval')


    models = {
        u'jset.tmplval': {
            'Meta': {'object_name': 'TmplVal'},
            'cdt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'udt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['jset']