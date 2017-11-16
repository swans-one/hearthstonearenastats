from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G

from hearthstonearenastats.app.card.models import Card
from hearthstonearenastats.app.draft.models import Draft, DraftPick, Game


class DraftValidationTest(TestCase):
    def setUp(self):
        self.user = G(User)

    def test_valid_entry(self):
        Draft.objects.create(
            user=self.user,
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
                user=self.user,
                first_hero='druid',
                second_hero='hunter',
                third_hero='mage',
                hero_choice='warlock',
            )


class DraftPickValidationTest(TestCase):
    def setUp(self):
        self.card_1 = G(Card)
        self.card_2 = G(Card)
        self.card_3 = G(Card)
        self.card_4 = G(Card)
        self.draft = G(Draft)

    def test_valid_entry(self):
        DraftPick.objects.create(
            draft=self.draft,
            pick_number=1,
            first=self.card_1,
            second=self.card_2,
            third=self.card_3,
            choice=self.card_1,
        )
        self.assertEqual(DraftPick.objects.count(), 1)

    def test_invlaid_card_choice(self):
        with self.assertRaises(ValidationError):
            DraftPick.objects.create(
                draft=self.draft,
                pick_number=1,
                first=self.card_1,
                second=self.card_2,
                third=self.card_3,
                choice=self.card_4,
            )

    def test_invalid_number_choice(self):
        with self.assertRaises(ValidationError):
            DraftPick.objects.create(
                draft=self.draft,
                pick_number=40,
                first=self.card_1,
                second=self.card_2,
                third=self.card_3,
                choice=self.card_1,
            )


class GameValidationTest(TestCase):
    def setUp(self):
        self.draft = G(Draft)

    def test_valid_game(self):
        Game.objects.create(
            draft=self.draft,
            opponent_hero='mage',
            game_number=1,
            won=True,
            coin=True,
            mulligan_count=4
        )
        self.assertEqual(Game.objects.count(), 1)

    def test_invalid_muligans_coin(self):
        with self.assertRaises(ValidationError):
            Game.objects.create(
                draft=self.draft,
                opponent_hero='mage',
                game_number=1,
                won=True,
                coin=True,
                mulligan_count=5
            )

    def test_invalid_muligans_no_coint(self):
        with self.assertRaises(ValidationError):
            Game.objects.create(
                draft=self.draft,
                opponent_hero='mage',
                game_number=1,
                won=True,
                coin=False,
                mulligan_count=4
            )

    def test_invalid_game_number(self):
        with self.assertRaises(ValidationError):
            Game.objects.create(
                draft=self.draft,
                opponent_hero='mage',
                game_number=15,
                won=True,
                coin=False,
                mulligan_count=3
            )
