import argparse
import getpass
from itertools import cycle

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from src.protection_defenders.core.mixins import CheckUserMailMixin
from src.protection_defenders.defenders_app.tests.factories import LanguageFactory, FormFactory, BlockFactory, \
    QuestionFactory, FormAnswerFactory, AnswerFactory


class DictAppendAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        try:
            (key, value) = values[0].split("=", 2)
        except ValueError:
            raise argparse.ArgumentError(self, f"could not parse argument \"{values[0]}\" as key=value format")
        parser_dict = getattr(args, self.dest) or {}
        parser_dict[key] = value
        setattr(args, self.dest, parser_dict)


class Command(CheckUserMailMixin, BaseCommand):
    help = 'Create fake data for development environment'

    @staticmethod
    def create_languages(languages_dict: dict = None):
        languages_dict = languages_dict or {'english': 'en', 'spanish': 'sp'}
        languages_objects = [LanguageFactory.create(name=key, code=value) for key, value in languages_dict.items()]
        languages = cycle(languages_objects)
        return languages

    @staticmethod
    def create_block():
        color = Faker().color(luminosity='light')
        block = BlockFactory.create(color=color)
        return block

    def create_questions(self, amount: int, user, language):
        block = self.create_block()
        form = FormFactory.create(language=language)
        questions = QuestionFactory.create_batch(amount, block=block, form=form)
        form_answers = FormAnswerFactory.create_batch(amount, form=form, user=user)

        return questions, form_answers

    def create_answers(self, amount: int, user, language):
        questions, form_answers = self.create_questions(amount=amount, user=user, language=language)
        answers_length = len(questions)
        unique_random_answers = [Faker().unique.text() for i in range(answers_length)]

        for i in range(answers_length):
            plain_text = unique_random_answers[i]
            value_u = user.crypt_and_verify_from_cipher(value=plain_text)
            value_a = user.init_a.crypt_and_verify_from_cipher(value=plain_text)
            AnswerFactory.create(question=questions[i], form_answer=form_answers[i], value_u=value_u, value_a=value_a)

    def check_if_email_user_exists(self, email: str) -> str:
        validated_email = self.check_login_mail(email=email)
        if validated_email is not None:
            self.stdout.write(self.style.SUCCESS(f'Getting {email} user in database'))
            email = validated_email
        return email

    def get_or_register(self, email: str, is_admin: bool = None, password: str = None, **kwargs):
        is_admin = is_admin or False
        if is_admin is True:
            kwargs['is_superuser'] = True
            kwargs['is_staff'] = True
        checked_email = self.check_if_email_user_exists(email=email)
        user, created = get_user_model().objects.get_or_create(email=checked_email, **kwargs)
        if created is True:
            self.stdout.write(self.style.SUCCESS(f'Registering {user.get_short_name} user'))
            user.set_password(password)
            user.save()
        return user

    def get_or_create_users(self, users: list = None, admin_users: list = None, password: str = None):
        for user in admin_users:
            self.get_or_register(email=user, password=password, is_admin=True)
        user_objects = [self.get_or_register(email=user, password=password) for user in users]
        return user_objects

    def create_data(self, amount: int, usernames: list, admin_usernames: list, languages: cycle, passwd: str = None):
        users = self.get_or_create_users(users=usernames, admin_users=admin_usernames, password=passwd)
        for user in users:
            language = next(languages)
            self.create_answers(amount=amount, user=user, language=language)
            self.stdout.write(self.style.SUCCESS(f'{user.get_short_name} created {amount} answers successfully'))

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int, nargs='?', help="Amount of questions/answer per user", default=5)
        parser.add_argument('-p', '--passwd', action='store_true', help='Activate set passwd')
        parser.add_argument('-a', '--admins', nargs='+', help="Set admin usernames",
                            default=["admin@admin.com", "admin2@admin2.com"])
        parser.add_argument('-u', '--users', nargs='+', help="Set usernames",
                            default=["user@user.com", "user2@user.com"])
        parser.add_argument("-l", '--languages', nargs='+', action=DictAppendAction, metavar="KEY=VALUE",
                            help="Set languages")

    def handle(self, *args, **kwargs):
        languages = self.create_languages(languages_dict=kwargs['languages'])
        passwd = "1Password-strong-strong-very-strong"
        if kwargs['passwd'] is True:
            passwd = getpass.getpass()
        self.create_data(amount=kwargs['amount'], usernames=kwargs['users'], admin_usernames=kwargs['admins'],
                         languages=languages, passwd=passwd)
        return self.stdout.write(self.style.SUCCESS(f'Finished'))
