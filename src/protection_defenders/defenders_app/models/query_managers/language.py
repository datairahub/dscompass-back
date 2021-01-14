from django.db import models

from src.protection_defenders.core.mixins import IsActiveFilterMixin


class LanguageQuerySet(models.QuerySet, IsActiveFilterMixin):
    pass
