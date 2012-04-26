# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserPreferences'
        db.create_table('alpha_userpreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updateMethod', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
        ))
        db.send_create_signal('alpha', ['UserPreferences'])

        # Adding model 'HousePreferences'
        db.create_table('alpha_housepreferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_zone', self.gf('django.db.models.fields.CharField')(default='EST', max_length=3)),
        ))
        db.send_create_signal('alpha', ['HousePreferences'])

        # Adding model 'HMCreator'
        db.create_table('alpha_hmcreator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('alpha', ['HMCreator'])

        # Adding model 'Person'
        db.create_table('alpha_person', (
            ('hmcreator_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HMCreator'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('cell_phone', self.gf('django.db.models.fields.TextField')(max_length=10, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('settings', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.UserPreferences'], unique=True)),
        ))
        db.send_create_signal('alpha', ['Person'])

        # Adding model 'Tag'
        db.create_table('alpha_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('alpha', ['Tag'])

        # Adding model 'Vendor'
        db.create_table('alpha_vendor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('alpha', ['Vendor'])

        # Adding M2M table for field tags on 'Vendor'
        db.create_table('alpha_vendor_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vendor', models.ForeignKey(orm['alpha.vendor'], null=False)),
            ('tag', models.ForeignKey(orm['alpha.tag'], null=False))
        ))
        db.create_unique('alpha_vendor_tags', ['vendor_id', 'tag_id'])

        # Adding model 'House'
        db.create_table('alpha_house', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('settings', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HousePreferences'], unique=True)),
        ))
        db.send_create_signal('alpha', ['House'])

        # Adding M2M table for field vendor_list on 'House'
        db.create_table('alpha_house_vendor_list', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('house', models.ForeignKey(orm['alpha.house'], null=False)),
            ('vendor', models.ForeignKey(orm['alpha.vendor'], null=False))
        ))
        db.create_unique('alpha_house_vendor_list', ['house_id', 'vendor_id'])

        # Adding M2M table for field tag_list on 'House'
        db.create_table('alpha_house_tag_list', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('house', models.ForeignKey(orm['alpha.house'], null=False)),
            ('tag', models.ForeignKey(orm['alpha.tag'], null=False))
        ))
        db.create_unique('alpha_house_tag_list', ['house_id', 'tag_id'])

        # Adding model 'ApprovalCode'
        db.create_table('alpha_approvalcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.House'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.Person'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('targetPerson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('inviteString', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('alpha', ['ApprovalCode'])

        # Adding model 'Residency'
        db.create_table('alpha_residency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_set', to=orm['alpha.Person'])),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.House'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('approvalCode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.ApprovalCode'], null=True, blank=True)),
            ('rent_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('alpha', ['Residency'])

        # Adding model 'HMChatter'
        db.create_table('alpha_hmchatter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.HMCreator'])),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.House'], null=True, blank=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('timeCreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('timeModified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_set', blank=True, null=True, to=orm['alpha.HMChatter'])),
            ('transaction_parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transaction_child_set', blank=True, null=True, to=orm['alpha.HMTransaction'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('publicly_editable', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('alpha', ['HMChatter'])

        # Adding M2M table for field tag on 'HMChatter'
        db.create_table('alpha_hmchatter_tag', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hmchatter', models.ForeignKey(orm['alpha.hmchatter'], null=False)),
            ('tag', models.ForeignKey(orm['alpha.tag'], null=False))
        ))
        db.create_unique('alpha_hmchatter_tag', ['hmchatter_id', 'tag_id'])

        # Adding model 'HMPoll'
        db.create_table('alpha_hmpoll', (
            ('hmchatter_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HMChatter'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('alpha', ['HMPoll'])

        # Adding model 'PollOption'
        db.create_table('alpha_polloption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.HMCreator'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='option_set', to=orm['alpha.HMPoll'])),
            ('option_text', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('alpha', ['PollOption'])

        # Adding model 'SingleVotePoll'
        db.create_table('alpha_singlevotepoll', (
            ('hmpoll_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HMPoll'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('alpha', ['SingleVotePoll'])

        # Adding model 'ExcellencePoll'
        db.create_table('alpha_excellencepoll', (
            ('hmpoll_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HMPoll'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('alpha', ['ExcellencePoll'])

        # Adding model 'PollResponse'
        db.create_table('alpha_pollresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.Person'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.PollOption'])),
        ))
        db.send_create_signal('alpha', ['PollResponse'])

        # Adding model 'HMTransaction'
        db.create_table('alpha_hmtransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.HMCreator'])),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.House'], null=True, blank=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('timeCreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('timeModified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.HMTransaction'], null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal('alpha', ['HMTransaction'])

        # Adding M2M table for field tag on 'HMTransaction'
        db.create_table('alpha_hmtransaction_tag', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hmtransaction', models.ForeignKey(orm['alpha.hmtransaction'], null=False)),
            ('tag', models.ForeignKey(orm['alpha.tag'], null=False))
        ))
        db.create_unique('alpha_hmtransaction_tag', ['hmtransaction_id', 'tag_id'])

        # Adding model 'Debt'
        db.create_table('alpha_debt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.Person'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.HMTransaction'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('alpha', ['Debt'])

        # Adding model 'Purchase'
        db.create_table('alpha_purchase', (
            ('hmtransaction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HMTransaction'], unique=True, primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.Vendor'])),
        ))
        db.send_create_signal('alpha', ['Purchase'])

        # Adding model 'Settlement'
        db.create_table('alpha_settlement', (
            ('hmtransaction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['alpha.HMTransaction'], unique=True, primary_key=True)),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.Person'])),
        ))
        db.send_create_signal('alpha', ['Settlement'])

        # Adding model 'Alert'
        db.create_table('alpha_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_alert', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_alerts', blank=True, null=True, to=orm['alpha.Alert'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.Person'])),
            ('house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alpha.House'], null=True, blank=True)),
            ('template_path', self.gf('django.db.models.fields.CharField')(default='test_alert.html', max_length=100)),
            ('related_objects', self.gf('livewith.fields.PickledObjectField')(null=True, protocol=2)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('acknowledged', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('alpha', ['Alert'])


    def backwards(self, orm):
        
        # Deleting model 'UserPreferences'
        db.delete_table('alpha_userpreferences')

        # Deleting model 'HousePreferences'
        db.delete_table('alpha_housepreferences')

        # Deleting model 'HMCreator'
        db.delete_table('alpha_hmcreator')

        # Deleting model 'Person'
        db.delete_table('alpha_person')

        # Deleting model 'Tag'
        db.delete_table('alpha_tag')

        # Deleting model 'Vendor'
        db.delete_table('alpha_vendor')

        # Removing M2M table for field tags on 'Vendor'
        db.delete_table('alpha_vendor_tags')

        # Deleting model 'House'
        db.delete_table('alpha_house')

        # Removing M2M table for field vendor_list on 'House'
        db.delete_table('alpha_house_vendor_list')

        # Removing M2M table for field tag_list on 'House'
        db.delete_table('alpha_house_tag_list')

        # Deleting model 'ApprovalCode'
        db.delete_table('alpha_approvalcode')

        # Deleting model 'Residency'
        db.delete_table('alpha_residency')

        # Deleting model 'HMChatter'
        db.delete_table('alpha_hmchatter')

        # Removing M2M table for field tag on 'HMChatter'
        db.delete_table('alpha_hmchatter_tag')

        # Deleting model 'HMPoll'
        db.delete_table('alpha_hmpoll')

        # Deleting model 'PollOption'
        db.delete_table('alpha_polloption')

        # Deleting model 'SingleVotePoll'
        db.delete_table('alpha_singlevotepoll')

        # Deleting model 'ExcellencePoll'
        db.delete_table('alpha_excellencepoll')

        # Deleting model 'PollResponse'
        db.delete_table('alpha_pollresponse')

        # Deleting model 'HMTransaction'
        db.delete_table('alpha_hmtransaction')

        # Removing M2M table for field tag on 'HMTransaction'
        db.delete_table('alpha_hmtransaction_tag')

        # Deleting model 'Debt'
        db.delete_table('alpha_debt')

        # Deleting model 'Purchase'
        db.delete_table('alpha_purchase')

        # Deleting model 'Settlement'
        db.delete_table('alpha_settlement')

        # Deleting model 'Alert'
        db.delete_table('alpha_alert')


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
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.TextField', [], {'max_length': '10', 'blank': 'True'}),
            'hmcreator_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.HMCreator']", 'unique': 'True', 'primary_key': 'True'}),
            'settings': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['alpha.UserPreferences']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
        }
    }

    complete_apps = ['alpha']
