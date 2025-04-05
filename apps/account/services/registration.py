import logging

from django.utils.translation import gettext_lazy as _

from apps.account.models import EmailVerificationCode, User
from apps.common.services.email import EmailService

logger = logging.getLogger("apps")


class UserRegistration:
    def __init__(self, email, password, first_name="", last_name="", phone_number="", group_names=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.group_names = group_names or ["User"]
        self.user = None
        self.verification_code = None

    def is_email_taken(self):
        return User.objects.filter(email=self.email).exists()

    def create_user(self):
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            group_names=self.group_names,
            is_email_verified=False,
        )
        logger.info(f"User created: {self.email}")

    def create_verification_code(self):
        self.verification_code = EmailVerificationCode.create_verification_code(self.user)
        logger.info(f"Verification code created for: {self.email}")

    def send_verification_email(self):
        EmailService.send_email_verification_code(self.verification_code)
        logger.info(f"Verification email sent to: {self.email}")

    def register(self):
        if self.is_email_taken():
            logger.warning(f"Registration failed. Email already in use: {self.email}")
            raise ValueError(_("User with this email already exists"))

        self.create_user()
        self.create_verification_code()
        self.send_verification_email()

        return self.user, self.verification_code
