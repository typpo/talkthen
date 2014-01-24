# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhoneNumber'
        db.create_table(u'core_phonenumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, blank=True)),
        ))
        db.send_create_signal(u'core', ['PhoneNumber'])

        # Adding model 'Call'
        db.create_table(u'core_call', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PhoneNumber'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('scheduled_for', self.gf('django.db.models.fields.DateTimeField')()),
            ('called', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('canceled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirmation_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Call'])

        # Adding M2M table for field participant_numbers on 'Call'
        m2m_table_name = db.shorten_name(u'core_call_participant_numbers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('call', models.ForeignKey(orm[u'core.call'], null=False)),
            ('phonenumber', models.ForeignKey(orm[u'core.phonenumber'], null=False))
        ))
        db.create_unique(m2m_table_name, ['call_id', 'phonenumber_id'])


    def backwards(self, orm):
        # Deleting model 'PhoneNumber'
        db.delete_table(u'core_phonenumber')

        # Deleting model 'Call'
        db.delete_table(u'core_call')

        # Removing M2M table for field participant_numbers on 'Call'
        db.delete_table(db.shorten_name(u'core_call_participant_numbers'))


    models = {
        u'core.call': {
            'Meta': {'object_name': 'Call'},
            'called': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmation_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner_number': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.PhoneNumber']"}),
            'participant_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'call_participants'", 'symmetrical': 'False', 'to': u"orm['core.PhoneNumber']"}),
            'scheduled_for': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'core.phonenumber': {
            'Meta': {'object_name': 'PhoneNumber'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['core']