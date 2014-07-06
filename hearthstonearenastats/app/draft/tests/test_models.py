from django.core.exceptions import ValidationError
from django.test import TestCase
from django_dynamic_fixture import G

from hearthstonearenastats.app.account.models import Account
from hearthstonearenastats.app.draft.models import Draft


class DraftValidationTest(TestCase):
    def setUp(self):
        self.account = G(Account)

    def test_valid_entry(self):
        Draft.objects.create(
            account=self.account,
            first_hero='druid',
            second_hero='hunter',
            third_hero='mage',
            hero_choice='mage',
        )
        self.assertEqual(Draft.objects.count(), 1)

    def test_saves_date(self):
        draft = G(Draft, start_date=None)
        self.assertIsNotNone(draft.start_date)

    def test_invalid_hero_choice(self):
        with self.assertRaises(ValidationError):
            Draft.objects.create(
                account=self.account,
                first_hero='druid',
                second_hero='hunter',
                third_hero='mage',
                hero_choice='warlock',
            )
