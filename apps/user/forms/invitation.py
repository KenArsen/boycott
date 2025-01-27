from django import forms

from apps.user.choices import RoleChoices
from apps.user.models import Invitation


class InvitationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=RoleChoices)

    class Meta:
        model = Invitation
        fields = ["email", "role"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Invitation.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email
