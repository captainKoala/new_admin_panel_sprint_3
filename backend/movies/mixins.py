import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(
        verbose_name=_('TimeStampedMixin.created'),
        help_text=_('TimeStampedMixin.created.help_text'),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name=_('TimeStampedMixin.modified'),
        help_text=_('TimeStampedMixin.modified.help_text'),
        auto_now=True,
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        verbose_name='UUIDMixin.ID',
        help_text='UUIDMixin.ID.help_text',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
