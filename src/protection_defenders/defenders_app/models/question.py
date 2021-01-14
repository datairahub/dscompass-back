from django.db import models
from django.utils.translation import gettext_lazy as _

from .query_managers.question import QuestionQuerySet


class Block(models.Model):
    name = models.CharField(default='', unique=True, max_length=128, verbose_name=_(u'Name of this block'))
    display_name = models.CharField(default='', max_length=128, verbose_name=_(u'Display name of this block'))
    color = models.CharField(default='', max_length=128, verbose_name=_(u'Color of this block'))
    order = models.IntegerField(null=True, unique=True, verbose_name=_(u'Order of this block'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creation timestamp'))

    def __str__(self):
        return f"{self.name} - {self.display_name}"

    class Meta:
        app_label = 'defenders_app'
        verbose_name = _(u'Block')
        verbose_name_plural = _(u'Blocks')


class Question(models.Model):
    order = models.IntegerField(null=True, verbose_name=_(u'Order of this question'))
    block = models.ForeignKey(Block, on_delete=models.CASCADE, verbose_name=_(u'Block related'),
                              related_name='block_question_related')
    form = models.ForeignKey('Form', on_delete=models.CASCADE, verbose_name=_(u'Form related'),
                             related_name='question_related')
    question = models.TextField(default='', verbose_name=_(u'Question text'))
    default_response = models.TextField(default='', blank=True, verbose_name=_(u'Default response'))
    context = models.TextField(default='', blank=True, verbose_name=_(u'Question context'))
    example = models.TextField(default='', blank=True, verbose_name=_(u'Question example'))
    more_info = models.TextField(default='', blank=True, verbose_name=_(u'More info of this question'))
    image = models.ImageField(default='', blank=True, verbose_name=_(u'Question image'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creation timestamp'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_(u'Last modification timestamp'))
    is_active = models.BooleanField(blank=True, default=True, db_index=True, verbose_name=_(u'Is active?'))
    related_question = models.ForeignKey("self", blank=True, null=True, on_delete=models.DO_NOTHING,
                                         verbose_name=_(u'Question related'), related_name='question_related')

    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return f"{self.question}"

    class Meta:
        app_label = 'defenders_app'
        verbose_name = _(u'Question')
        verbose_name_plural = _(u'Questions')


class QuestionFile(models.Model):
    file = models.FileField()
    name = models.CharField(default='', max_length=128, verbose_name=_(u'File name'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='files')
    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Creation timestamp'))
    is_active = models.BooleanField(blank=True, default=True, db_index=True, verbose_name=_(u'Is active?'))

    class Meta:
        app_label = 'defenders_app'
        verbose_name = _(u'File')
        verbose_name_plural = _(u'Files')
