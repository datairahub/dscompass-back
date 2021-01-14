from django.db import models

from src.protection_defenders.core.mixins import IsActiveFilterMixin


class FormQuerySet(models.QuerySet, IsActiveFilterMixin):
    pass


class FormAnswerQuerySet(FormQuerySet):
    pass
