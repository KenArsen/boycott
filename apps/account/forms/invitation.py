from django import forms

from apps.account.choices import RoleChoices
from apps.account.models import Invitation


class InvitationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=RoleChoices)

    class Meta:
        model = Invitation
        fields = ["email", "role"]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if self.instance.pk:
            if (
                Invitation.objects.filter(email=email)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise forms.ValidationError("Этот email уже зарегистрирован.")
        else:
            if Invitation.objects.filter(email=email).exists():
                raise forms.ValidationError("Этот email уже зарегистрирован.")

        return email
