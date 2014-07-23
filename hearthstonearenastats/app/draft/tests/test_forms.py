from datetime import datetime

from django.test import TestCase
from django_dynamic_fixture import G

from hearthstonearenastats.app.card.models import Card, Patch
from hearthstonearenastats.app.draft import forms as draft_forms
from hearthstonearenastats.app.draft.models import Draft


class DraftPickFormTest(TestCase):
    def setUp(self):
        p = G(Patch)
        card_1 = G(Card, patch=p, hero='neutral', collectible=True)
        card_2 = G(Card, patch=p, hero='neutral', collectible=True)
        card_3 = G(Card, patch=p, hero='neutral', collectible=True)
        self.form_data = {
            'choice_1': card_1.id,
            'choice_2': card_2.id,
            'choice_3': card_3.id,
            'choosen': 'card1',
        }

    def test_validation(self):
        d = G(Draft)
        form = draft_forms.DraftPickForm(self.form_data, draft_id=d.id)
        self.assertTrue(form.is_valid())


class PrizesFormTest(TestCase):
    def setUp(self):
        pass


class GetCardQsTest(TestCase):
    def setUp(self):
        patch = G(Patch)
        patch_old = G(Patch, datetime)
        self.draft = G(Draft, first_hero='mage', hero_choice='mage')
        self.neutral_card = G(
            Card, hero='neutral', collectible=True, patch=patch)
        self.mage_card = G(
            Card, hero='mage', collectible=True, patch=patch)
        self.druid_card = G(
            Card, hero='druid', collectible=True, patch=patch)
        self.rando_card = G(
            Card, hero='druid', collectible=False, patch=patch)
        self.old_card = G(
            Card, hero='druid', collectible=False, patch=patch_old)

    def test_includes_neutrals(self):
        qs = draft_forms.get_card_qs(self.draft.id)
        self.assertIn(self.neutral_card, list(qs))

    def test_includes_draft_hero(self):
        qs = draft_forms.get_card_qs(self.draft.id)
        self.assertIn(self.mage_card, list(qs))

    def test_excludes_others(self):
        qs = draft_forms.get_card_qs(self.draft.id)
        self.assertNotIn(self.druid_card, list(qs))

    def test_excludes_non_collectibles(self):
        qs = draft_forms.get_card_qs(self.draft.id)
        self.assertNotIn(self.rando_card, list(qs))

    def test_excludes_other_patches(self):
        qs = draft_forms.get_card_qs(self.draft.id)
        self.assertNotIn(self.old_card, list(qs))
