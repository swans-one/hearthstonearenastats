# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DraftStatus.account'
        db.delete_column(u'draft_draftstatus', 'account_id')

        # Adding field 'DraftStatus.user'
        db.add_column(u'draft_draftstatus', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User'], unique=True),
                      keep_default=False)

        # Adding field 'DraftStatus.draft'
        db.add_column(u'draft_draftstatus', 'draft',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['draft.Draft'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'DraftStatus.account'
        db.add_column(u'draft_draftstatus', 'account',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['account.Account'], unique=True),
                      keep_default=False)

        # Deleting field 'DraftStatus.user'
        db.delete_column(u'draft_draftstatus', 'user_id')

        # Deleting field 'DraftStatus.draft'
        db.delete_column(u'draft_draftstatus', 'draft_id')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'draft.draft': {
            'Meta': {'object_name': 'Draft'},
            'completed_draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed_games': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_hero': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'hero_choice': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'second_hero': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'third_hero': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'draft.draftpick': {
            'Meta': {'object_name': 'DraftPick'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['card.Card']"}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['draft.Draft']"}),
            'first': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['card.Card']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pick_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'second': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['card.Card']"}),
            'third': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['card.Card']"})
        },
        u'draft.draftstatus': {
            'Meta': {'object_name': 'DraftStatus'},
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['draft.Draft']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'draft.game': {
            'Meta': {'object_name': 'Game'},
            'coin': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['draft.Draft']"}),
            'game_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mulligan_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'opponent_hero': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'won': ('django.db.models.fields.BooleanField', [], {})
        },
        u'draft.prizes': {
            'Meta': {'object_name': 'Prizes'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'prize_cards'", 'symmetrical': 'False', 'to': u"orm['card.Card']"}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['draft.Draft']"}),
            'dust': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'gold': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'golden_cards': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'golden_prize_cards'", 'symmetrical': 'False', 'to': u"orm['card.Card']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_packs': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['draft']