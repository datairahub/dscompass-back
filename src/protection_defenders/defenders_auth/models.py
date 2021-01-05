import uuid
from typing import Tuple, Dict, Any

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.functional import cached_property
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from . import fields
from .managers import UserManager
from ..core.get_cipher_user import AdminCipher
from ...datacrypter.rsa_crypter.cipher import RSADataCrypt, RSADataDecrypt
from ...datacrypter.rsa_crypter.keys import RSAKeysGenerator, RsaKeys
from ...datacrypter.rsa_crypter.signer import RSASigner, RSAVerifier


class User(AbstractBaseUser, PermissionsMixin):
    email = fields.TextEmailField(verbose_name=_('Email Address'))
    register_email = models.CharField(max_length=254, unique=True, default=uuid.uuid4)
    is_active = models.BooleanField(default=True, verbose_name=_('Is active?'))
    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False)
    created = models.DateTimeField(auto_now=True, verbose_name=_('Created timestamp'))
    modified = models.DateTimeField(auto_now_add=True, verbose_name=_('Modified timestamp'))
    public_key = models.TextField(default='', verbose_name=_('Public Key'))
    private_key = models.TextField(default='', verbose_name=_('Private Key'))

    objects = UserManager()

    USERNAME_FIELD = 'register_email'
    EMAIL_FIELD = 'register_email'

    class Meta:
        app_label = 'defenders_auth'
        db_table = 'auth_user'

        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"User {self.pk}"

    def get_full_name(self):
        return self.email

    @cached_property
    def init_a(self):
        return AdminCipher(actual_user=self).get_cipher()

    @cached_property
    def _get_mail(self) -> Tuple[str, bytes]:
        return self.send_signature_to_cipher_and_decrypt_value(value=self.email)

    @cached_property
    def get_short_name(self):
        return self._get_mail

    @staticmethod
    def generate_rsa_keys(secret: str = None) -> Dict[Any, str]:
        rsa_secret = secret or settings.CIPHER_KEY
        rsa_key_gen = RSAKeysGenerator(passphrase=rsa_secret)
        return rsa_key_gen().value_dict

    def get_keys(self, private_key: str = None, public_key: str = None):
        private = private_key or self.private_key
        public = public_key or self.public_key
        return RsaKeys(value_dict={"privKey": private, "pubKey": public})

    def crypt_and_verify_from_cipher(self, value: str, private_key: str = None, public_key: str = None,
                                     secret_signer: str = None, passphrase: str = None) -> str:
        secret_sign = secret_signer or settings.CIPHER_KEY
        secret_passphrase = passphrase or settings.SECRET_KEY
        keys = self.get_keys(private_key=private_key, public_key=public_key)

        cipher_service = RSADataCrypt(passphrase=secret_passphrase, secret_signer=secret_sign)
        encrypted_data, signature = cipher_service(value=value.encode(), keys=keys).data
        verifier = RSAVerifier(passphrase=secret_sign, signature=signature)
        is_verified = verifier(keys=keys)

        if is_verified is True:
            return encrypted_data
        return value

    def send_signature_to_cipher_and_decrypt_value(self, value: str, private_key: str = None, public_key: str = None,
                                                   secret_signer: str = None) -> Tuple[str, bytes]:
        secret_sign = secret_signer or settings.CIPHER_KEY
        keys = self.get_keys(private_key=private_key, public_key=public_key)

        signer = RSASigner(passphrase=secret_sign)
        signature = signer(keys=keys)
        cipher_service = RSADataDecrypt(passphrase=settings.SECRET_KEY, secret_signer=secret_sign)
        decrypted_value = cipher_service(value=value.encode(), keys=keys, signature=signature)

        return decrypted_value.data

    @staticmethod
    def send_user_email(context: dict, subject_template_name: str, email_template_name: str,
                        from_email: str, to_email: str or bytes):
        subject = loader.render_to_string(template_name=subject_template_name, context=context)
        email_subject = ''.join(subject.splitlines())
        email_body = loader.render_to_string(template_name=email_template_name, context=context)

        email = EmailMultiAlternatives(subject=email_subject, body=email_body, from_email=from_email, to=[to_email])
        email.send()

    def send_token_email(self, uri, subject_template_name, email_template_name, generator_token):
        # Only admin users get reset password mail
        from_email = settings.DEFAULT_FROM_EMAIL
        admin = User.objects.filter(is_superuser=True).first()
        user_email = admin.get_short_name

        context = {
            'email': user_email,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'user': self,
            'token': generator_token.make_token(user=self),
            'url': uri
        }
        self.send_user_email(context=context, subject_template_name=subject_template_name,
                             email_template_name=email_template_name, from_email=from_email, to_email=user_email)

    def send_activation_notification(self, subject_template_name, email_template_name):
        from_email = settings.DEFAULT_FROM_EMAIL
        user_email = self.get_short_name

        context = {
            'email': user_email,
            'user': self,
        }
        self.send_user_email(context=context, subject_template_name=subject_template_name,
                             email_template_name=email_template_name, from_email=from_email,
                             to_email=user_email)

    def save(self, *args, **kwargs):
        # Only for new users
        if self._state.adding is True:
            rsa_keys = self.generate_rsa_keys()
            self.private_key = rsa_keys['privKey']
            self.public_key = rsa_keys['pubKey']

            encrypted_email = self.crypt_and_verify_from_cipher(value=self.email)
            self.email = encrypted_email
        super(User, self).save(*args, **kwargs)
