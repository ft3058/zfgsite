# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PermLog'
        db.create_table(u'jperm_permlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('results', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('is_success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_finish', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'jperm', ['PermLog'])

        # Adding model 'PermSudo'
        db.create_table(u'jperm_permsudo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('commands', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'jperm', ['PermSudo'])

        # Adding model 'PermRole'
        db.create_table(u'jperm_permrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('key_path', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'jperm', ['PermRole'])

        # Adding M2M table for field sudo on 'PermRole'
        m2m_table_name = db.shorten_name(u'jperm_permrole_sudo')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('permrole', models.ForeignKey(orm[u'jperm.permrole'], null=False)),
            ('permsudo', models.ForeignKey(orm[u'jperm.permsudo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['permrole_id', 'permsudo_id'])

        # Adding model 'PermRule'
        db.create_table(u'jperm_permrule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'jperm', ['PermRule'])

        # Adding M2M table for field asset on 'PermRule'
        m2m_table_name = db.shorten_name(u'jperm_permrule_asset')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('permrule', models.ForeignKey(orm[u'jperm.permrule'], null=False)),
            ('asset', models.ForeignKey(orm[u'jasset.asset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['permrule_id', 'asset_id'])

        # Adding M2M table for field asset_group on 'PermRule'
        m2m_table_name = db.shorten_name(u'jperm_permrule_asset_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('permrule', models.ForeignKey(orm[u'jperm.permrule'], null=False)),
            ('assetgroup', models.ForeignKey(orm[u'jasset.assetgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['permrule_id', 'assetgroup_id'])

        # Adding M2M table for field user on 'PermRule'
        m2m_table_name = db.shorten_name(u'jperm_permrule_user')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('permrule', models.ForeignKey(orm[u'jperm.permrule'], null=False)),
            ('user', models.ForeignKey(orm[u'juser.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['permrule_id', 'user_id'])

        # Adding M2M table for field user_group on 'PermRule'
        m2m_table_name = db.shorten_name(u'jperm_permrule_user_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('permrule', models.ForeignKey(orm[u'jperm.permrule'], null=False)),
            ('usergroup', models.ForeignKey(orm[u'juser.usergroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['permrule_id', 'usergroup_id'])

        # Adding M2M table for field role on 'PermRule'
        m2m_table_name = db.shorten_name(u'jperm_permrule_role')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('permrule', models.ForeignKey(orm[u'jperm.permrule'], null=False)),
            ('permrole', models.ForeignKey(orm[u'jperm.permrole'], null=False))
        ))
        db.create_unique(m2m_table_name, ['permrule_id', 'permrole_id'])

        # Adding model 'PermPush'
        db.create_table(u'jperm_permpush', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='perm_push', to=orm['jasset.Asset'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='perm_push', to=orm['jperm.PermRole'])),
            ('is_public_key', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_password', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('result', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'jperm', ['PermPush'])


    def backwards(self, orm):
        # Deleting model 'PermLog'
        db.delete_table(u'jperm_permlog')

        # Deleting model 'PermSudo'
        db.delete_table(u'jperm_permsudo')

        # Deleting model 'PermRole'
        db.delete_table(u'jperm_permrole')

        # Removing M2M table for field sudo on 'PermRole'
        db.delete_table(db.shorten_name(u'jperm_permrole_sudo'))

        # Deleting model 'PermRule'
        db.delete_table(u'jperm_permrule')

        # Removing M2M table for field asset on 'PermRule'
        db.delete_table(db.shorten_name(u'jperm_permrule_asset'))

        # Removing M2M table for field asset_group on 'PermRule'
        db.delete_table(db.shorten_name(u'jperm_permrule_asset_group'))

        # Removing M2M table for field user on 'PermRule'
        db.delete_table(db.shorten_name(u'jperm_permrule_user'))

        # Removing M2M table for field user_group on 'PermRule'
        db.delete_table(db.shorten_name(u'jperm_permrule_user_group'))

        # Removing M2M table for field role on 'PermRule'
        db.delete_table(db.shorten_name(u'jperm_permrule_role'))

        # Deleting model 'PermPush'
        db.delete_table(u'jperm_permpush')


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
            'domains': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['jasset.Domains']", 'symmetrical': 'False', 'blank': 'True'}),
            'env': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['jasset.AssetGroup']", 'symmetrical': 'False', 'blank': 'True'}),
            'group1': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['jasset.AssetGroup1']", 'symmetrical': 'False', 'blank': 'True'}),
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
        u'jasset.assetgroup': {
            'Meta': {'object_name': 'AssetGroup'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'jasset.assetgroup1': {
            'Meta': {'object_name': 'AssetGroup1'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jasset.AssetGroup']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'jasset.domains': {
            'Meta': {'object_name': 'Domains'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path1': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path2': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path3': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path4': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path5': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path6': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path7': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'path8': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
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
        u'jperm.permlog': {
            'Meta': {'object_name': 'PermLog'},
            'action': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'results': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        u'jperm.permpush': {
            'Meta': {'object_name': 'PermPush'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'perm_push'", 'to': u"orm['jasset.Asset']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_password': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public_key': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'result': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'perm_push'", 'to': u"orm['jperm.PermRole']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'jperm.permrole': {
            'Meta': {'object_name': 'PermRole'},
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sudo': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'perm_role'", 'symmetrical': 'False', 'to': u"orm['jperm.PermSudo']"})
        },
        u'jperm.permrule': {
            'Meta': {'object_name': 'PermRule'},
            'asset': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'perm_rule'", 'symmetrical': 'False', 'to': u"orm['jasset.Asset']"}),
            'asset_group': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'perm_rule'", 'symmetrical': 'False', 'to': u"orm['jasset.AssetGroup']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'perm_rule'", 'symmetrical': 'False', 'to': u"orm['jperm.PermRole']"}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'perm_rule'", 'symmetrical': 'False', 'to': u"orm['juser.User']"}),
            'user_group': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'perm_rule'", 'symmetrical': 'False', 'to': u"orm['juser.UserGroup']"})
        },
        u'jperm.permsudo': {
            'Meta': {'object_name': 'PermSudo'},
            'commands': ('django.db.models.fields.TextField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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

    complete_apps = ['jperm']