from datetime import datetime
import json

from django.core.management import BaseCommand, CommandError

from hearthstone.app.card.models import Card, Patch


class Command(BaseCommand):
    args = "<JSON card database>"

    def handle(*args, **options):
        if not args:
            raise CommandError("Path to JSON card database required.")
        file_name = args[0]
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
    pass
