from django.contrib import admin

from src.protection_defenders.defenders_auth.forms import DefendersAdminAuthenticationForm


class ProtectInterDefendersAppAdminSite(admin.AdminSite):
    site_title = 'DS-Compass - Protection International'
    site_header = 'DS-Compass - Protection International'
    login_form = DefendersAdminAuthenticationForm
