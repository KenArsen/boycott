from django.contrib.auth import login
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.account.choices import RoleChoices
from apps.account.forms.registration import RegistrationForm
from apps.account.models import Invitation


class RegisterByInvitationView(FormView):
    template_name = "account/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("admin:index")

    def dispatch(self, request, *args, **kwargs):
        try:
            self.invitation = Invitation.objects.get(code=kwargs["code"], is_used=False)
        except Invitation.DoesNotExist:
            raise Http404("Приглашение не найдено или уже использовано")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["email"] = self.invitation.email
        return initial

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = self.invitation.email
        user.set_password(form.cleaned_data["password"])
        user.role = self.invitation.role
        user.is_staff = user.role.name in [RoleChoices.MODERATOR, RoleChoices.ADMIN]
        if user.role.name == RoleChoices.ADMIN:
            user.is_superuser = True
        user.save()

        # Связываем пользователя с приглашением
        self.invitation.user = user
        self.invitation.is_used = True
        self.invitation.save()

        login(self.request, user)
        return super().form_valid(form)
