# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.permissions import BasePermission


def is_authenticated(user):
    """
    Check if user is authenticated and active
    """
    return bool(
        user and
        user.is_authenticated and
        user.is_active)


class IsAuthenticatedAndActive(BasePermission):
    """
    Allows access only to authenticated and active users.
    """
    def has_permission(self, request, view):
        return bool(
            request.path in settings.NOAUTH_URLS or
            is_authenticated(request.user))