from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.choices import RoleChoices
from apps.common.models import CoreModel


class UserManager(BaseUserManager):
    """
    Custom account manager that defines methods for creating regular users
    and superusers.
    """

    def create_user(self, email, password=None, role_name=RoleChoices.USER, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        role = Role.objects.get(name=role_name)  # Получаем роль из модели Role
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_moderator(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, password, RoleChoices.MODERATOR, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, RoleChoices.ADMIN, **extra_fields)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Role Name"))
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        verbose_name=_("Permissions"),
        help_text=_("Select permissions associated with this role"),
    )

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.name


class User(CoreModel, AbstractUser):
    """Пользовательский модель"""

    username = None

    role = models.ForeignKey(
        to=Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Role"),
        related_name="users",
    )
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    first_name = models.CharField(max_length=255, blank=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, blank=True, verbose_name=_("Last Name"))
    phone_number = models.CharField(max_length=255, blank=True, verbose_name=_("Phone Number"))

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

    def is_admin(self):
        return self.role.name == RoleChoices.ADMIN

    def is_moderator(self):
        return self.role.name.lower() == RoleChoices.MODERATOR
