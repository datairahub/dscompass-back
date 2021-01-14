from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms.widgets import TextInput
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from .models import Form, FormAnswer, Block, Question, QuestionFile, Language


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    fields = (
        'name', 'language', 'display_name', 'introduction', 'conclusion', 'created', 'questions_length', 'is_active',)
    readonly_fields = ('questions_length', 'created',)
    list_display = ('name', 'display_name', 'is_active',)
    search_fields = ('name', 'display_name',)


@admin.register(FormAnswer)
class FormAnswerAdmin(admin.ModelAdmin):
    fields = ('form', 'user', 'name', 'created', 'modified', 'user_answers',)
    readonly_fields = ('form', 'user', 'name', 'created', 'modified', 'user_answers',)
    list_display = ('id', 'form', 'user', 'name', 'modified',)
    list_select_related = ('form', 'user',)
    search_fields = ('form__name', 'user__email')
    ordering = ('form',)

    @staticmethod
    def user_answers(obj):
        answer = obj.f_answer_related.first()
        admin_cipher = obj.user.init_a
        value_a = admin_cipher.get_value(answer=answer)

        text = f"<strong>{answer.question.question}</strong><br>" \
               f"{value_a}<br><br>"
        return format_html(text)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class QuestionBlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ('name', 'display_name', 'color', 'order')
        readonly_fields = ('id', 'created',)
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }


class QuestionBlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'color', 'created',)
    search_fields = ('name', 'order', 'color', 'created',)
    form = QuestionBlockForm


admin.site.register(Block, QuestionBlockAdmin)


class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('form', 'block', 'question', 'default_response', 'context', 'example', 'more_info',
                  'order', 'related_question', 'image', 'is_active',)
        readonly_fields = ('id', 'created', 'modified',)
        widgets = {
            'context': TinyMCE,
            'example': TinyMCE,
            'more_info': TinyMCE,
        }


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionModelForm
    list_display = ('question', 'block', 'form', 'order', 'created', 'is_active',)
    list_select_related = ('block', 'form',)
    search_fields = ('form__name', 'question',)

    class Media:
        css = {
            'all': ('/static/css/admin-styles.css',)
        }


admin.site.register(Question, QuestionAdmin)


@admin.register(QuestionFile)
class QuestionFileAdmin(admin.ModelAdmin):
    fields = ('name', 'file', 'question', 'is_active',)
    readonly_fields = ('created',)
    list_display = ('name', 'file', 'created', 'is_active')
    list_select_related = ('question',)
    search_fields = ('name', 'created')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fields = ('name', 'code', 'file', 'is_active',)
    list_display = ('name', 'code', 'file', 'is_active')
    search_fields = ('name', 'code')


admin.site.unregister(Group)
