import logging
import uuid
from datetime import timedelta

from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.account.models import User

logger = logging.getLogger("apps")


def default_expiration():
    return timezone.now() + timedelta(days=7)


class Invitation(models.Model):
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("Invitation Code"),
    )
    is_used = models.BooleanField(default=False, verbose_name=_("Is Used"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    expires_at = models.DateTimeField(
        default=default_expiration,
        verbose_name=_("Expires At"),
        help_text=_("Date and time when the invitation expires"),
    )
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        verbose_name=_("Group"),
        help_text=_("Group assigned to the user upon registration"),
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Registered User"),
        related_name="invitation",
    )

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.group.name})"

    def get_invitation_url(self):
        return reverse("account:registration-with-invite", kwargs={"code": self.code})

    def is_expired(self):
        expired = timezone.now() > self.expires_at
        logger.debug(f"Checking if invitation {self.code} is expired: {expired}")
        return expired

    def is_valid(self):
        valid = not self.is_used and not self.is_expired()
        logger.debug(f"Checking if invitation {self.code} is valid: {valid}")
        return valid

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=["is_used"])
        logger.info(f"Invitation {self.code} marked as used for {self.email}")
