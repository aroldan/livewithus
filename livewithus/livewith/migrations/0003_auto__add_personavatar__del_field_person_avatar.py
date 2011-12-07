# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PersonAvatar'
        db.create_table('alpha_personavatar', (
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('crop_from', self.gf('django.db.models.fields.CharField')(default='center', max_length=10, blank=True)),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(related_name='personavatar_related', blank=True, null=True, to=orm['photologue.PhotoEffect'])),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(related_name='avatar', unique=True, primary_key=True, to=orm['alpha.Person'])),
        ))
        db.send_create_signal('alpha', ['PersonAvatar'])

        # Deleting field 'Person.avatar'
        db.delete_column('alpha_person', 'avatar')


    def backwards(self, orm):
        
        # Deleting model 'PersonAvatar'
        db.delete_table('alpha_personavatar')

        # Adding field 'Person.avatar'
        db.add_column('alpha_person', 'avatar', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True), keep_default=False)


    models = {
        'alpha.alert': {
            'Meta': {'object_name': 'Alert'},
            'acknowledged': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.House']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_alert': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_alerts'", 'blank': 'True', 'null': 'True', 'to': "orm['alpha.Alert']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"}),
            'related_objects': ('livewith.fields.PickledObjectField', [], {'null': 'True', 'protocol': '2'}),
            'template_path': ('django.db.models.fields.CharField', [], {'default': "'test_alert.html'", 'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
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
        'alpha.debt': {
            'Meta': {'object_name': 'Debt'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.HMTransaction']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        'alpha.excellencepoll': {
            'Meta': {'object_name': 'ExcellencePoll', '_ormbases': ['alpha.HMPoll']},
            'hmpoll_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMPoll']", 'unique': 'True', 'primary_key': 'True'})
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
        'alpha.hmpoll': {
            'Meta': {'object_name': 'HMPoll', '_ormbases': ['alpha.HMChatter']},
            'hmchatter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMChatter']", 'unique': 'True', 'primary_key': 'True'})
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
            'cell_phone': ('django.db.models.fields.TextField', [], {'max_length': '10', 'blank': 'True'}),
            'hmcreator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMCreator']", 'unique': 'True', 'primary_key': 'True'}),
            'settings': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.UserPreferences']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'alpha.personavatar': {
            'Meta': {'object_name': 'PersonAvatar'},
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'personavatar_related'", 'blank': 'True', 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'avatar'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['alpha.Person']"}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'alpha.polloption': {
            'Meta': {'object_name': 'PollOption'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.HMCreator']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option_text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'option_set'", 'to': "orm['alpha.HMPoll']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'alpha.pollresponse': {
            'Meta': {'object_name': 'PollResponse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.PollOption']"})
        },
        'alpha.purchase': {
            'Meta': {'object_name': 'Purchase', '_ormbases': ['alpha.HMTransaction']},
            'hmtransaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMTransaction']", 'unique': 'True', 'primary_key': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Vendor']"})
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
        'alpha.settlement': {
            'Meta': {'object_name': 'Settlement', '_ormbases': ['alpha.HMTransaction']},
            'hmtransaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMTransaction']", 'unique': 'True', 'primary_key': 'True'}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alpha.Person']"})
        },
        'alpha.singlevotepoll': {
            'Meta': {'object_name': 'SingleVotePoll', '_ormbases': ['alpha.HMPoll']},
            'hmpoll_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMPoll']", 'unique': 'True', 'primary_key': 'True'})
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
        'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.59999999999999998'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['alpha']
