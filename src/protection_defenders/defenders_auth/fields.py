from django.core import validators
from django.db.models import TextField
from django import forms
from django.utils.translation import gettext_lazy as _


class TextEmailField(TextField):
    default_validators = [validators.validate_email]
    description = _("Email address")

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.EmailField,
            **kwargs,
        })
