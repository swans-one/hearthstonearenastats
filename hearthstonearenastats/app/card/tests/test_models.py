from datetime import datetime

from django.test import TestCase
from django_dynamic_fixture import G, N

from hearthstonearenastats.app.card.models import Card, Patch


class CurrentPatchCardManagerTest(TestCase):
    def setUp(self):
        self.patch_old = G(Patch, db_update_date=datetime(2014, 1, 1))
        self.patch_new = G(Patch, db_update_date=datetime(2014, 2, 2))
        G(Card, patch=self.patch_new)
        G(Card, patch=self.patch_new)
        G(Card, patch=self.patch_old)
        G(Card, patch=self.patch_old)

    def test_queryset_filters_old_patches(self):
        self.assertEqual(Card.current_patch.count(), 2)

    def test_queryset_returns_new_patches(self):
        patches = [c.patch for c in Card.current_patch.all()]
        all_cards_new_patch = all([p == self.patch_new for p in patches])
        self.assertTrue(all_cards_new_patch)


class CardUnicodeTest(TestCase):
    def test_name_and_mana(self):
        card = N(Card, name='My Test Card', mana=4)
        expected_unicode = 'My Test Card :: 4M'
        self.assertEqual(expected_unicode, card.__unicode__())

    def test_name_and_no_mana(self):
        card = N(Card, name='My Test Card', mana=None)
        expected_unicode = 'My Test Card :: -M'
        self.assertEqual(expected_unicode, card.__unicode__())


class PatchUnicodeTest(TestCase):
    def test_patch_unicode(self):
        patch = N(Patch, patch_version='1.1.1.0')
        expected_unicode = '1.1.1.0'
        self.assertEqual(expected_unicode, patch.__unicode__())
