from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.choices import RoleChoices


class UserManager(BaseUserManager):
    """
    Custom user manager that defines methods for creating regular users
    and superusers.
    """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.role = RoleChoices.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None

    role = models.CharField(
        max_length=20,
        choices=RoleChoices,
        default=RoleChoices.MODERATOR,
        verbose_name=_("Role"),
    )
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    first_name = models.CharField(
        max_length=255, blank=True, verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=255, blank=True, verbose_name=_("Last Name")
    )
    phone_number = models.CharField(
        max_length=255, blank=True, verbose_name=_("Phone Number")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
