from django.contrib import messages
from django.shortcuts import redirect, render

from apps.account.forms.authentication import EmailVerificationForm, UserRegistrationForm
from apps.account.models import EmailVerificationCode, User
from apps.account.services.registration import UserRegistration


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                registration = UserRegistration(
                    email=data["email"],
                    password=data["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone_number=data["phone_number"],
                )
                user, code = registration.register()
                request.session["user"] = str(user.pk)
                messages.success(request, "Registration successful! Check your email for a code.")
                return redirect("account:verify-email")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = UserRegistrationForm()
    return render(request, "pages/auth/registration.html", {"form": form})


def verify_email_view(request):
    from uuid import UUID

    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        user_id = UUID(request.session["user"])
        user = User.objects.get(pk=user_id)

        if form.is_valid():
            code = form.cleaned_data["code"].strip()
            try:
                verification = EmailVerificationCode.objects.get(user=user, code=code)
                if verification.is_expired():
                    messages.error(request, "Срок действия кода истек.")
                else:
                    verification.user.email_verified = True
                    verification.user.save()
                    verification.delete()
                    messages.success(request, "Email успешно подтвержден!")
                    return redirect("home")
            except EmailVerificationCode.DoesNotExist:
                messages.error(request, "Неверный код.")
    else:
        form = EmailVerificationForm()

    return render(request, "pages/auth/verify_email.html", {"form": form})
