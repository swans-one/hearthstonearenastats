from django.conf import settings
from django.db import models
from timezone_field import TimezoneField


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    timezone = TimezoneField(default='US/Eastern')
