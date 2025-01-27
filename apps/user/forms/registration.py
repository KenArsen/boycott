from django import forms

from apps.user.models import User


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}),
        label="Подтвердите пароль",
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
            self.add_error("confirm_password", "Пароли не совпадают!")

        return cleaned_data
