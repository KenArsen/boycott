import uuid  # noqa: TC003

from django.db import models
from django.utils.translation import gettext_lazy as _


class CoreModel(models.Model):
    """
    Abstract base model with common fields for all models.
    """

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("Active"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk}"

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save(
                update_fields=(
                    ["is_active", "updated_at"] if not self._state.adding else None
                )
            )

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save(
                update_fields=(
                    ["is_active", "updated_at"] if not self._state.adding else None
                )
            )
