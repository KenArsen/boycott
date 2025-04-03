import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from apps.account.models import Invitation

logger = logging.getLogger("apps")


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["email", "group"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        # Проверяем, существует ли уже приглашение с таким email (исключая текущий экземпляр)
        if (
            Invitation.objects.filter(email=email)
            .exclude(pk=self.instance.pk or None)
            .exists()
        ):
            logger.warning(f"Attempt to invite already invited email: {email}")
            raise forms.ValidationError(_("This email is already invited."))
        logger.debug(f"Email {email} validated successfully")
        return email
