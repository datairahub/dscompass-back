from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Reset answers values from different admin user'

    def search_answers_and_reset_cipher(self, admin_user_id, user):
        form_answers = user.u_answer_owner.all()
        for f_answers in form_answers:
            answers = f_answers.f_answer_related.all()
            for answer in answers:
                old_admin_cipher_user = user.init_a
                value = old_admin_cipher_user.get_value(answer=answer)
                answer.value_a = old_admin_cipher_user.crypt_and_verify_from_cipher(value=value)
                answer.save()
                self.stdout.write(self.style.SUCCESS(f'User ID: {admin_user_id} change {answer} value successfully'))

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='Username of new admin user cipher')

    def handle(self, *args, **kwargs):
        user_model = get_user_model()
        user_id = kwargs['user_id']

        try:
            admin_user = user_model.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist, ValidationError):
            return self.stdout.write(self.style.ERROR('User ID: {user_id} doest not exist in database'))

        if admin_user.is_superuser is False:
            return self.stdout.write(self.style.ERROR(f'User ID: {user_id} is not a superuser'))
        if admin_user.is_active is False:
            self.stdout.write(self.style.WARNING(f'User ID: {user_id} is not an active user'))

        self.stdout.write(self.style.SUCCESS(f'User ID: {user_id} is superuser'))
        all_users = user_model.objects.all()
        for user in all_users:
            self.search_answers_and_reset_cipher(admin_user_id=user_id, user=user)
