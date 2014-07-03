import os

from django.core.management import call_command
from django.test import TestCase
from mock import patch

from hearthstonearenastats.app.card.models import Patch, Card
from hearthstonearenastats.app.card.management.commands.import_cards import (
    get_or_create_patch, bulk_insert_cards
)


class ImportCardsTest(TestCase):
    def setUp(self):
        path = './hearthstonearenastats/app/card/tests/card_db_sample.json'
        self.db_file_name = os.path.realpath(path)

    def test_works(self):
        call_command('import_cards', filename=self.db_file_name)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Card.objects.count(), 2)

    def test_idempotency(self):
        call_command('import_cards', filename=self.db_file_name)
        call_command('import_cards', filename=self.db_file_name)
        self.assertEqual(Patch.objects.count(), 1)
        self.assertEqual(Card.objects.count(), 2)


class GetOrCreatePatchTest(TestCase):
    def test_created(self):
        patch = {'patch': '10.1.1.1.a'}
        patch, created = get_or_create_patch(patch)
        self.assertTrue(created)

    def test_already_exists(self):
        patch = {'patch': '10.1.1.1.a'}
        get_or_create_patch(patch)
        patch, created = get_or_create_patch(patch)
        self.assertFalse(created)
