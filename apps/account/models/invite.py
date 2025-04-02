import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.account.choices import RoleChoices
from apps.account.models.user import Role, User


class Invitation(models.Model):
    email = models.EmailField(unique=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(
        to=Role,
        on_delete=models.CASCADE,
        default=RoleChoices.MODERATOR,
        verbose_name=_("Role"),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Registered User"),
    )

    def __str__(self):
        return f"{self.email} ({self.role.name})"

    def get_invitation_url(self):
        return reverse("account:registration-with-invite", kwargs={"code": self.code})
