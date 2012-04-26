# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HMUtility'
        db.create_table('utilities_hmutility', (
            ('hmcreator_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HMCreator'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('utilities', ['HMUtility'])

        # Adding model 'UtilityHouseSettings'
        db.create_table('utilities_utilityhousesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.House'])),
            ('utility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utilities.HMUtility'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('utilities', ['UtilityHouseSettings'])

        # Adding model 'UtilityPersonSettings'
        db.create_table('utilities_utilitypersonsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.Person'])),
            ('utility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utilities.HMUtility'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('utilities', ['UtilityPersonSettings'])


    def backwards(self, orm):
        
        # Deleting model 'HMUtility'
        db.delete_table('utilities_hmutility')

        # Deleting model 'UtilityHouseSettings'
        db.delete_table('utilities_utilityhousesettings')

        # Deleting model 'UtilityPersonSettings'
        db.delete_table('utilities_utilitypersonsettings')


    models = {
        'alpha.approvalcode': {
            'Meta': {'object_name': 'ApprovalCode'},
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviteString': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"}),
            'targetPerson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'alpha.hmcreator': {
            'Meta': {'object_name': 'HMCreator'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'alpha.house': {
            'Meta': {'object_name': 'House'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alpha.Person']", 'through': "orm['alpha.Residency']", 'symmetrical': 'False'}),
            'settings': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HousePreferences']", 'unique': 'True'}),
            'tag_list': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alpha.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'vendor_list': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alpha.Vendor']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'alpha.housepreferences': {
            'Meta': {'object_name': 'HousePreferences'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'default': "'EST'", 'max_length': '3'})
        },
        'alpha.person': {
            'Meta': {'object_name': 'Person', '_ormbases': ['alpha.HMCreator']},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.TextField', [], {'max_length': '10', 'blank': 'True'}),
            'hmcreator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMCreator']", 'unique': 'True', 'primary_key': 'True'}),
            'settings': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.UserPreferences']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'alpha.residency': {
            'Meta': {'object_name': 'Residency'},
            'approvalCode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.ApprovalCode']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_set'", 'to': "orm['alpha.Person']"}),
            'rent_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        'alpha.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alpha.userpreferences': {
            'Meta': {'object_name': 'UserPreferences'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updateMethod': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'})
        },
        'alpha.vendor': {
            'Meta': {'object_name': 'Vendor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alpha.Tag']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'utilities.hmutility': {
            'Meta': {'object_name': 'HMUtility', '_ormbases': ['alpha.HMCreator']},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'hmcreator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMCreator']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'utilities.utilityhousesettings': {
            'Meta': {'object_name': 'UtilityHouseSettings'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.House']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utilities.HMUtility']"})
        },
        'utilities.utilitypersonsettings': {
            'Meta': {'object_name': 'UtilityPersonSettings'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utilities.HMUtility']"})
        }
    }

    complete_apps = ['utilities']
