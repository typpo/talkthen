# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Call.remind_at'
        db.add_column(u'core_call', 'remind_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 26, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Call.remind_at'
        db.delete_column(u'core_call', 'remind_at')


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
            'participant_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'call_participant_numbers'", 'symmetrical': 'False', 'to': u"orm['core.PhoneNumber']"}),
            'remind_at': ('django.db.models.fields.DateTimeField', [], {}),
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