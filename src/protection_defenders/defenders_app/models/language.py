from django.db import models
from django.utils.translation import gettext_lazy as _

from .query_managers.language import LanguageQuerySet


class Language(models.Model):
    name = models.CharField(default='', unique=True, max_length=128, verbose_name=_(u'Language name'))
    code = models.CharField(default='', max_length=2, verbose_name=_(u'Language code (2 chars)'))
    file = models.FileField()
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_(u'Is active?'))
    
    objects = LanguageQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        app_label = 'defenders_app'
        verbose_name = _(u'Language')
        verbose_name_plural = _(u'Languages')
