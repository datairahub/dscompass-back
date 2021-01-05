from django.db import models
from django.utils.translation import gettext_lazy as _

from .query_managers.answer import AnswerQueryset


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name=_(u'Question related'),
                                 related_name='q_answer_related')
    form_answer = models.ForeignKey('FormAnswer', on_delete=models.CASCADE, verbose_name=_(u'Form related'),
                                    related_name='f_answer_related')
    value_u = models.TextField(default='', verbose_name=_(u'Answer'))
    value_a = models.TextField(default='', verbose_name=_(u'Answer'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creation timestamp'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_(u'Last modification timestamp'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_(u'Is active?'))

    objects = AnswerQueryset.as_manager()

    def __str__(self):
        return f"{self.question} - {self.form_answer}"

    class Meta:
        app_label = 'defenders_app'
        verbose_name = _(u'Answer')
        verbose_name_plural = _(u'Answers')
