# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Card'
        db.create_table(u'card_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['card.Patch'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('hero', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('card_set', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('mana', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attack', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('health', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('collectible', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'card', ['Card'])

        # Adding model 'Patch'
        db.create_table(u'card_patch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patch_version', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('db_update_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'card', ['Patch'])


    def backwards(self, orm):
        # Deleting model 'Card'
        db.delete_table(u'card_card')

        # Deleting model 'Patch'
        db.delete_table(u'card_patch')


    models = {
        u'card.card': {
            'Meta': {'object_name': 'Card'},
            'attack': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'card_set': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'collectible': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'health': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hero': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mana': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'patch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['card.Patch']"}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        u'card.patch': {
            'Meta': {'object_name': 'Patch'},
            'db_update_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patch_version': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['card']