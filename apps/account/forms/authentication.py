from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from apps.account.models import User


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    password_confirm = forms.CharField(widget=forms.PasswordInput, label=_("Confirm Password"))
    first_name = forms.CharField(max_length=255, required=False, label=_("First Name"))
    last_name = forms.CharField(max_length=255, required=False, label=_("Last Name"))
    phone_number = forms.CharField(max_length=255, required=False, label=_("Phone Number"))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("User with this email already exists."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(_("Passwords do not match."))

        return cleaned_data


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        label="Код подтверждения",
        max_length=6,
        min_length=6,
        validators=[RegexValidator(r"^\d{6}$", message="Код должен состоять из 6 цифр.")],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите 6-значный код",
                "inputmode": "numeric",
                "autocomplete": "one-time-code",
            }
        ),
    )

    def clean_code(self):
        code = self.cleaned_data["code"]
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError(_("Enter a valid 6-digit numeric code."))
        return code


class LoginForm(forms.Form):
    """
    Форма входа пользователя.
    """

    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)


class PasswordResetRequestForm(forms.Form):
    """
    Форма запроса сброса пароля.
    """

    email = forms.EmailField(label=_("Email"))


class PasswordResetForm(forms.Form):
    """
    Форма сброса пароля.
    """

    password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label=_("Confirm New Password"), widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match."))
        return password2


class PasswordChangeForm(forms.Form):
    """
    Форма изменения пароля.
    """

    old_password = forms.CharField(label=_("Current Password"), widget=forms.PasswordInput)
    password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label=_("Confirm New Password"), widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match."))
        return password2
