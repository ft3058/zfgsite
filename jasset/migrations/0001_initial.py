# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AssetGroup'
        db.create_table(u'jasset_assetgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
        ))
        db.send_create_signal(u'jasset', ['AssetGroup'])

        # Adding model 'IDC'
        db.create_table(u'jasset_idc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('bandwidth', self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True, blank=True)),
            ('linkman', self.gf('django.db.models.fields.CharField')(default='', max_length=16, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('network', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now=True, null=True, blank=True)),
            ('operator', self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'jasset', ['IDC'])

        # Adding model 'Asset'
        db.create_table(u'jasset_asset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('other_ip', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('use_default_auth', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('idc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jasset.IDC'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('mac', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('remote_ip', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cpu', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('memory', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('disk', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('system_type', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('system_version', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
            ('system_arch', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('cabinet', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('asset_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('env', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('check_code', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('passwd', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('udate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('type1', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('type2', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'jasset', ['Asset'])

        # Adding M2M table for field group on 'Asset'
        m2m_table_name = db.shorten_name(u'jasset_asset_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('asset', models.ForeignKey(orm[u'jasset.asset'], null=False)),
            ('assetgroup', models.ForeignKey(orm[u'jasset.assetgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['asset_id', 'assetgroup_id'])

        # Adding model 'AssetRecord'
        db.create_table(u'jasset_assetrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jasset.Asset'])),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('alert_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'jasset', ['AssetRecord'])

        # Adding model 'AssetAlias'
        db.create_table(u'jasset_assetalias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['juser.User'])),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jasset.Asset'])),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'jasset', ['AssetAlias'])


    def backwards(self, orm):
        # Deleting model 'AssetGroup'
        db.delete_table(u'jasset_assetgroup')

        # Deleting model 'IDC'
        db.delete_table(u'jasset_idc')

        # Deleting model 'Asset'
        db.delete_table(u'jasset_asset')

        # Removing M2M table for field group on 'Asset'
        db.delete_table(db.shorten_name(u'jasset_asset_group'))

        # Deleting model 'AssetRecord'
        db.delete_table(u'jasset_assetrecord')

        # Deleting model 'AssetAlias'
        db.delete_table(u'jasset_assetalias')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'jasset.asset': {
            'Meta': {'ordering': "['ip']", 'object_name': 'Asset'},
            'asset_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'cabinet': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'check_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'cpu': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'disk': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'env': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['jasset.AssetGroup']", 'symmetrical': 'False', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jasset.IDC']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'memory': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'other_ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'passwd': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'remote_ip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'system_arch': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'system_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'system_version': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'type1': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'type2': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'udate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'use_default_auth': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        u'jasset.assetalias': {
            'Meta': {'object_name': 'AssetAlias'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jasset.Asset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['juser.User']"})
        },
        u'jasset.assetgroup': {
            'Meta': {'object_name': 'AssetGroup'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'jasset.assetrecord': {
            'Meta': {'object_name': 'AssetRecord'},
            'alert_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jasset.Asset']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        u'jasset.idc': {
            'Meta': {'object_name': 'IDC'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'bandwidth': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkman': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'network': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'operator': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'juser.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['juser.UserGroup']", 'symmetrical': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'CU'", 'max_length': '2'}),
            'ssh_key_pwd': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'juser.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['jasset']