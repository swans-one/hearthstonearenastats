# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Prizes'
        db.create_table(u'draft_prizes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('draft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['draft.Draft'])),
            ('number_packs', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('gold', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('dust', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'draft', ['Prizes'])

        # Adding M2M table for field cards on 'Prizes'
        m2m_table_name = db.shorten_name(u'draft_prizes_cards')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('prizes', models.ForeignKey(orm[u'draft.prizes'], null=False)),
            ('card', models.ForeignKey(orm[u'card.card'], null=False))
        ))
        db.create_unique(m2m_table_name, ['prizes_id', 'card_id'])

        # Adding M2M table for field golden_cards on 'Prizes'
        m2m_table_name = db.shorten_name(u'draft_prizes_golden_cards')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('prizes', models.ForeignKey(orm[u'draft.prizes'], null=False)),
            ('card', models.ForeignKey(orm[u'card.card'], null=False))
        ))
        db.create_unique(m2m_table_name, ['prizes_id', 'card_id'])


    def backwards(self, orm):
        # Deleting model 'Prizes'
        db.delete_table(u'draft_prizes')

        # Removing M2M table for field cards on 'Prizes'
        db.delete_table(db.shorten_name(u'draft_prizes_cards'))

        # Removing M2M table for field golden_cards on 'Prizes'
        db.delete_table(db.shorten_name(u'draft_prizes_golden_cards'))


    models = {
        u'account.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'default': "'US/Eastern'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
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
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'})
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