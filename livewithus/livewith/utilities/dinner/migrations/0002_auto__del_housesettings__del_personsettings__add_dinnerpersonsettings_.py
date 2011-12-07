# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'HouseSettings'
        db.delete_table('dinner_housesettings')

        # Deleting model 'PersonSettings'
        db.delete_table('dinner_personsettings')

        # Adding model 'DinnerPersonSettings'
        db.create_table('dinner_dinnerpersonsettings', (
            ('utilitypersonsettings_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utilities.UtilityPersonSettings'], unique=True, primary_key=True)),
            ('notification_method', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('dinner', ['DinnerPersonSettings'])

        # Adding model 'DinnerHouseSettings'
        db.create_table('dinner_dinnerhousesettings', (
            ('utilityhousesettings_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utilities.UtilityHouseSettings'], unique=True, primary_key=True)),
            ('push_hour', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('push_minute', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('dinner', ['DinnerHouseSettings'])


    def backwards(self, orm):
        
        # Adding model 'HouseSettings'
        db.create_table('dinner_housesettings', (
            ('push_hour', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('utilityhousesettings_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utilities.UtilityHouseSettings'], unique=True, primary_key=True)),
            ('push_minute', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('dinner', ['HouseSettings'])

        # Adding model 'PersonSettings'
        db.create_table('dinner_personsettings', (
            ('notification_method', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
            ('utilitypersonsettings_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utilities.UtilityPersonSettings'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('dinner', ['PersonSettings'])

        # Deleting model 'DinnerPersonSettings'
        db.delete_table('dinner_dinnerpersonsettings')

        # Deleting model 'DinnerHouseSettings'
        db.delete_table('dinner_dinnerhousesettings')


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
        'alpha.hmchatter': {
            'Meta': {'object_name': 'HMChatter'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.HMCreator']"}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.House']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['alpha.HMChatter']"}),
            'publicly_editable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alpha.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timeCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timeModified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'transaction_parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transaction_child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['alpha.HMTransaction']"})
        },
        'alpha.hmcreator': {
            'Meta': {'object_name': 'HMCreator'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'alpha.hmtransaction': {
            'Meta': {'object_name': 'HMTransaction'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.HMCreator']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.House']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.HMTransaction']", 'null': 'True', 'blank': 'True'}),
            'purchase_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alpha.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'timeCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'timeModified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
            'cell_provider': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
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
        'dinner.dinnerhousesettings': {
            'Meta': {'object_name': 'DinnerHouseSettings', '_ormbases': ['utilities.UtilityHouseSettings']},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'push_hour': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'push_minute': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'utilityhousesettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['utilities.UtilityHouseSettings']", 'unique': 'True', 'primary_key': 'True'})
        },
        'dinner.dinneroption': {
            'Meta': {'object_name': 'DinnerOption'},
            'dinner_poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'option_set'", 'to': "orm['dinner.DinnerPoll']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option_text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'dinner.dinnerpersonsettings': {
            'Meta': {'object_name': 'DinnerPersonSettings', '_ormbases': ['utilities.UtilityPersonSettings']},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'notification_method': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'utilitypersonsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['utilities.UtilityPersonSettings']", 'unique': 'True', 'primary_key': 'True'})
        },
        'dinner.dinnerpoll': {
            'Meta': {'object_name': 'DinnerPoll', '_ormbases': ['alpha.HMChatter']},
            'hmchatter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMChatter']", 'unique': 'True', 'primary_key': 'True'})
        },
        'dinner.dinnerresponse': {
            'Meta': {'object_name': 'DinnerResponse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dinner.DinnerOption']"})
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
            'template': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utilities.HMUtility']"})
        },
        'utilities.utilitypersonsettings': {
            'Meta': {'object_name': 'UtilityPersonSettings'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'utility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utilities.HMUtility']"})
        }
    }

    complete_apps = ['dinner']
