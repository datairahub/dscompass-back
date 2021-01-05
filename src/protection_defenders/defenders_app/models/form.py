from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .language import Language
from .query_managers.form import FormQuerySet, FormAnswerQuerySet


class Form(models.Model):
    name = models.CharField(default='', unique=True, max_length=128, verbose_name=_(u'Name of this form'))
    display_name = models.CharField(default='', max_length=128, verbose_name=_(u'Display name of form'))
    questions_length = models.IntegerField(default=0, editable=False, verbose_name=_(u'Questions length of this form'))
    introduction = models.TextField(default='', verbose_name=_(u'Introduction text of this form'))
    conclusion = models.TextField(default='', verbose_name=_(u'Conclusion text of this form'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creation timestamp'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_(u'Is active?'))
    is_featured = models.BooleanField(default=True, db_index=True, verbose_name=_(u'Is featured?'))
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name=_(u'Language'),
                                 related_name='forms')

    objects = FormQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        app_label = 'defenders_app'
        verbose_name = _(u'Plan')
        verbose_name_plural = _(u'Plans')


class FormAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True,
                             verbose_name=_(u'User related'), related_name='u_answer_owner')
    form = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name=_(u'Related form'),
                             related_name='form_answer_related')
    name = models.CharField(default='', blank=True, max_length=256, verbose_name=_(u'Name of this plan'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creation timestamp'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_(u'Last modification timestamp'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_(u'Is active?'))

    objects = FormAnswerQuerySet.as_manager()

    def __str__(self):
        return f"{self.form}"

    class Meta:
        app_label = 'defenders_app'
        verbose_name = _(u'Answers')
        verbose_name_plural = _(u'Answers')
