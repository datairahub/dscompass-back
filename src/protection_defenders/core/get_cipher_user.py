from django.contrib.auth import get_user_model

from src.protection_defenders.defenders_app.models import Answer


class AdminCipher:
    def __init__(self, actual_user: get_user_model, answer: Answer = None,
                 public_key: str = None, private_key: str = None, value: str = None):
        self._user = actual_user
        self._answer = answer
        self.public_key = public_key
        self.private_key = private_key
        self.value = value

    def crypt_and_verify_from_cipher(self, *args, **kwargs):
        return self._user.crypt_and_verify_from_cipher(public_key=self.public_key,
                                                       private_key=self.private_key, *args, **kwargs)

    def get_value(self, answer: Answer = None) -> str:
        if answer == self._answer:
            return self.value
        return self._user.send_signature_to_cipher_and_decrypt_value(private_key=self.public_key,
                                                                     public_key=self.private_key,
                                                                     value=answer.value_a)

    def search_cipher_admin(self, admin_queryset):
        admin_user_keys = admin_queryset.filter(is_superuser=True, is_active=True).values('public_key', 'private_key')
        for keys in admin_user_keys:
            try:
                self.private_key = keys['private_key']
                self.public_key = keys['private_key']
                self.value = self._user.send_signature_to_cipher_and_decrypt_value(private_key=self.public_key,
                                                                                   public_key=self.private_key,
                                                                                   value=self._answer.value_a)
            except ValueError:
                ...
            return self

    def get_cipher(self):
        admin_users = get_user_model().objects
        answer_db = Answer.objects.first()
        if answer_db is not None:
            self._answer = answer_db
            return self.search_cipher_admin(admin_queryset=admin_users)

        default_user = admin_users.first()
        self.private_key = default_user.private_key
        self.public_key = default_user.private_key
        return self
