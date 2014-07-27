from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from timezone_field import TimeZoneField


class Account(models.Model):
    user = models.OneToOneField(User)
    timezone = TimeZoneField(default='US/Eastern')

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        account, created = Account.objects.get_or_create(user=instance)
