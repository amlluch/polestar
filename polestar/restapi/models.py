from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.

class Ships(models.Model):
    imo = models.CharField(_('imo'), max_length = 7, unique = True)
    name = models.CharField(_('name'), max_length = 100, blank=True, null=True)


class Positions(models.Model):
    ship = models.ForeignKey(Ships, null=True, blank=False, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(_('timestamp'), null=False, blank=False)
    latitude = models.DecimalField(_('latitude'), null=False, blank=False, max_digits=21, decimal_places=18)
    longitude = models.DecimalField(_('longitude'), null=False, blank=False, max_digits=21, decimal_places=18)


class Csv(models.Model):
    csvfile = models.FileField(_('CSV File'), upload_to=settings.UPLOAD_TO)
