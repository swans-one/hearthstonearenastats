from datetime import datetime
from optparse import make_option
import json

from django.core.management import BaseCommand, CommandError

from hearthstonearenastats.app.card.models import Card, Patch


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-f', '--filename',
            action='store',
            type='string',
            dest='filename',
        ),
    )

    def handle(*args, **options):
        if not options.get('filename'):
            raise CommandError("Path to JSON card database required.")
        file_name = options.get('filename')
        with open(file_name) as f:
            cards_json = json.load(f)
        patch = cards_json['meta']
        cards = cards_json['cards']
        patch_obj, created = get_or_create_patch(patch)
        if not created:
            return
        else:
            bulk_insert_cards(patch_obj, cards)


def get_or_create_patch(patch):
    """Given a spec of a patch, get or create it in the database.

    Args:
      - patch: a dictionary containing information about a patch.

    Returns:
      (patch_object, created)
    """
    patch_version = patch['patch']
    patch_obj, created = Patch.objects.get_or_create(
        patch_version=patch_version
    )
    if created:
        patch_obj.db_update_date = datetime.utcnow()
        patch_obj.save()
    return patch_obj, created


def bulk_insert_cards(patch_obj, cards):
    """Given a patch object, and a list of cards, put them in the db.

    Args:
      - patch_obj: a reference to a Patch object.
      - cards: a list of cards, imported from a json db.
    """
    Card.objects.bulk_create([
        Card(
            patch=patch_obj,
            name=card['name'],
            description=card['description'],
            hero=card['hero'],
            category=card['category'],
            quality=card['quality'],
            race=card['race'],
            card_set=card['set'],
            mana=card['mana'],
            attack=card['attack'],
            health=card['health'],
            collectible=card['collectible'],
        )
        for card in cards
    ])
