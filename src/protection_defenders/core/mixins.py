from django.contrib.auth import get_user_model


class IsActiveFilterMixin:
    def is_active(self):
        return self.filter(is_active=True)


class GetSerializerActionClassMixin:
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class CheckUserMailMixin:
    @staticmethod
    def check_login_mail(email):
        users = get_user_model().objects.filter(is_active=True)
        for user in users:
            user_email = user.get_short_name
            if user_email == email:
                return user.email
        return None
