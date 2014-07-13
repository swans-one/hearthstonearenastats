from datetime import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import utc

from hearthstonearenastats.app.card.models import Card
from hearthstonearenastats.app.account.models import Account

_hero_choices = (
    'druid', 'hunter', 'mage', 'paladin', 'priest',
    'rogue', 'shaman', 'warlock', 'warrior'
)
HERO_CHOICES = tuple(zip(_hero_choices, _hero_choices))


class DraftStatus(models.Model):
    STAGE_CHOICES = (('pick', 'Pick'), ('game', 'Game'))

    account = models.ForeignKey(Account, unique=True)
    stage = models.CharField(max_length=4, null=True, choices=STAGE_CHOICES)
    number = models.PositiveIntegerField(null=True)


class Draft(models.Model):
    user = models.ForeignKey(User)
    first_hero = models.CharField(max_length=8, choices=HERO_CHOICES)
    second_hero = models.CharField(max_length=8, choices=HERO_CHOICES)
    third_hero = models.CharField(max_length=8, choices=HERO_CHOICES)
    hero_choice = models.CharField(max_length=8, choices=HERO_CHOICES)
    start_date = models.DateTimeField(null=True)
    completed_draft = models.BooleanField(default=False)
    completed_games = models.BooleanField(default=False)

    def clean(self):
        choices = (self.first_hero, self.second_hero, self.third_hero)
        if self.hero_choice not in choices:
            msg = 'Hero choice {choice} not in {choices}.'
            raise ValidationError(
                msg.format(choice=self.hero_choice, choices=choices)
            )

    def save(self, *args, **kwargs):
        self.clean()
        if self.start_date is None:
            self.start_date = datetime.utcnow().replace(tzinfo=utc)
        super(Draft, self).save(*args, **kwargs)


class DraftPick(models.Model):
    draft = models.ForeignKey('Draft')
    pick_number = models.PositiveIntegerField()
    first = models.ForeignKey(Card, related_name='+')
    second = models.ForeignKey(Card, related_name='+')
    third = models.ForeignKey(Card, related_name='+')
    choice = models.ForeignKey(Card, related_name='+')

    def clean(self):
        choices = (self.first, self.second, self.third)
        if self.choice not in choices:
            msg = 'Choice {choice} not in {choices}'
            raise ValidationError(
                msg.format(choice=self.choice, choices=choices)
            )
        if self.pick_number > 30:
            msg = 'Pick number must be between 1 and 30'
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        self.clean()
        super(DraftPick, self).save(*args, **kwargs)


class Game(models.Model):
    draft = models.ForeignKey('Draft')
    opponent_hero = models.CharField(
        max_length=8, choices=HERO_CHOICES, null=True
    )
    game_number = models.PositiveIntegerField()
    won = models.BooleanField()
    coin = models.NullBooleanField(null=True)
    mulligan_count = models.PositiveIntegerField()

    def clean(self):
        extra_card_number = 1 if self.coin else 0
        max_mulligan = 3 + extra_card_number
        if self.mulligan_count > max_mulligan:
            msg = 'Can not mulligan more than {count} cards'
            raise ValidationError(msg.format(count=max_mulligan))
        if self.game_number > 14:
            msg = 'Game number must be between 1 and 14'
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        self.clean()
        super(Game, self).save(*args, **kwargs)
