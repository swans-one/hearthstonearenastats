from django.db import models

_hero_choices = (
    'neutral', 'druid', 'hunter', 'mage', 'paladin',
    'priest', 'rogue', 'shaman', 'warlock', 'warrior'
)
_race_choices = (
    'none', 'murloc', 'demon', 'totem', 'dragon', 'beast', 'pirate'
)
_category_choices = ('minion', 'weapon', 'spell', 'hero', 'ability')
_quality_choices = ('rare', 'free', 'uncommon', 'common', 'legendary', 'epic')
_card_set_choices = ('promotion', 'reward', 'missions', 'expert', 'basic')

CHOICES = {
    'hero': tuple(zip(_hero_choices, _hero_choices)),
    'category': tuple(zip(_category_choices, _category_choices)),
    'quality': tuple(zip(_quality_choices, _quality_choices)),
    'race': tuple(zip(_race_choices, _race_choices)),
    'card_set': tuple(zip(_card_set_choices, _card_set_choices)),
}


class CurrentPatchCardManager(models.Manager):
    def get_queryset(self):
        most_recent_patch = Patch.objects.all().order_by('-db_update_date')[0]
        qs = super(CurrentPatchCardManager, self).get_queryset()
        return qs.filter(patch=most_recent_patch)


class Card(models.Model):
    patch = models.ForeignKey('Patch')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    hero = models.CharField(max_length=8, choices=CHOICES['hero'])
    category = models.CharField(max_length=8, choices=CHOICES['category'])
    quality = models.CharField(max_length=12, choices=CHOICES['quality'])
    race = models.CharField(max_length=12, choices=CHOICES['race'])
    card_set = models.CharField(max_length=12, choices=CHOICES['card_set'])
    mana = models.IntegerField(null=True)
    attack = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    collectible = models.BooleanField()

    objects = models.Manager()
    current_patch = CurrentPatchCardManager()

    def __unicode__(self):
        name = self.name
        mana = str(self.mana) if self.mana is not None else "-"
        return "{name} :: {mana}M".format(name=name, mana=mana)


class Patch(models.Model):
    patch_version = models.CharField(max_length=32)
    db_update_date = models.DateField(null=True)

    def __unicode__(self):
        return self.patch_version
