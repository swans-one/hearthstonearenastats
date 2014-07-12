from django.test import TestCase
from django_dynamic_fixture import N

from hearthstonearenastats.app.card.models import Card, Patch


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
