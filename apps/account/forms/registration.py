import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from apps.account.models import User

logger = logging.getLogger("apps")


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Confirm password")}),
        label=_("Confirm password"),
        required=True,
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"readonly": "readonly"})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", _("Passwords do not match!"))
        return cleaned_data
