from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import DefendersUserCreationForm, DefendersUserChangeForm
from .models import User
from ..core.mixins import CheckUserMailMixin


class DefendersUserAdmin(CheckUserMailMixin, UserAdmin):
    fieldsets = (
        (None, {'fields': ('user_email', 'password',)}),
        (_('Permissions'), {
            'fields': ('is_active',),
        }),
        (_('Important dates'), {'fields': ('created', 'modified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('email', 'id', 'created', 'modified', 'user_email')
    add_form = DefendersUserCreationForm
    form = DefendersUserChangeForm
    model = User
    list_display = ('id', 'is_active',)
    ordering = ('email',)

    @staticmethod
    def user_email(user):
        return user.send_signature_to_cipher_and_decrypt_value(value=user.email)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        email_is_valid = self.check_login_mail(email=search_term)
        if email_is_valid is not None:
            queryset |= self.model.objects.filter(email=email_is_valid)
        return queryset, use_distinct


admin.site.register(User, DefendersUserAdmin)
admin.site.site_url = settings.APP_FRONTEND_URL
