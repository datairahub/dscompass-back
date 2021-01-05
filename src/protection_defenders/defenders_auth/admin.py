from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import DefendersUserCreationForm, DefendersUserChangeForm
from .models import User
from ..core.mixins import CheckUserMailMixin


class DefendersUserAdmin(CheckUserMailMixin, UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('created', 'modified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('id', 'created', 'modified',)
    add_form = DefendersUserCreationForm
    form = DefendersUserChangeForm
    model = User
    list_display = ('id', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        email_is_valid = self.check_login_mail(email=search_term)
        if email_is_valid is not None:
            queryset |= self.model.objects.filter(email=email_is_valid)
        return queryset, use_distinct


admin.site.register(User, DefendersUserAdmin)
admin.site.site_url = settings.APP_FRONTEND_URL
