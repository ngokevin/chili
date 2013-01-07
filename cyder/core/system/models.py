from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models, IntegrityError
from django.db.models.query import QuerySet
from django.db.models.signals import post_save

from cyder.base.mixins import ObjectUrlMixin
from cyder.base.models import BaseModel

import ipaddr

class System(BaseModel, ObjectUrlMixin):
    YES_NO_CHOICES = (
        (0, 'No'),
        (1, 'Yes'),
    )
    hostname = models.CharField(unique=True, max_length=255)
    department = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    class Meta:
        db_table = 'system'
        unique_together = ('hostname','location')

    def update_attrs(self):
        self.attrs = SystemKeyValue.objects.filter(system=self)
"""
class SystemKeyValue(CommonOption):
    system = models.ForiegnKey(System, null=False)
    aux_attrs = (
        ('description', 'A description of the Syste'),
    )
    def save(self, *args, **kwargs):
        self.clean()
        super(SystemKeyValue, self).save(*args, **kwargs)
"""
