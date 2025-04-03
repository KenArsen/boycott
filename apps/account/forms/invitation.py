from django import forms
from django.utils.translation import gettext_lazy as _

from apps.account.models import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["email", "group"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if (
            Invitation.objects.filter(email=email)
            .exclude(pk=self.instance.pk or None)
            .exists()
        ):
            raise forms.ValidationError(_("This email is already invited."))
        return email
