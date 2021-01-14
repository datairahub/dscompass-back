from django.db import models

from src.protection_defenders.core.mixins import IsActiveFilterMixin


class AnswerQueryset(IsActiveFilterMixin, models.QuerySet):
    def user_owner(self, user):
        return self.is_active().filter(form_answer__user=user)
