from django.contrib.admin.apps import AdminConfig


class ProtectionInternationalDefendersAdminConfig(AdminConfig):
    default_site = 'src.protection_defenders.project_admin.ProtectInterDefendersAppAdminSite'
