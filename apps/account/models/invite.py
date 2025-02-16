import uuid

from django.db import models
from django.urls import reverse


class Invitation(models.Model):
    email = models.EmailField(unique=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def get_invitation_url(self):
        return reverse("account:registration-with-invite", kwargs={"code": self.code})
