from django.contrib.auth import login
from django.contrib.auth.models import Group, Permission
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.account.forms.registration import RegistrationForm
from apps.account.models import Invitation


class RegisterByInvitationView(FormView):
    template_name = "account/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("admin:index")

    def dispatch(self, request, *args, **kwargs):
        """Проверка кода приглашения перед обработкой запроса."""
        try:
            self.invitation = Invitation.objects.get(code=kwargs["code"], is_used=False)
        except Invitation.DoesNotExist:
            raise Http404("Приглашение не найдено или уже использовано")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Передает email из приглашения в форму."""
        initial = super().get_initial()
        initial["email"] = self.invitation.email
        return initial

    def form_valid(self, form):
        """Обработка данных при успешной валидации формы."""
        user = form.save(commit=False)
        user.email = self.invitation.email
        user.set_password(form.cleaned_data["password"])
        user.is_staff = True
        user.save()

        manager_group, _ = Group.objects.get_or_create(name="Managers")
        user.groups.add(manager_group)

        permissions = Permission.objects.filter(
            codename__in=["view_user", "change_user"]
        )
        user.user_permissions.add(*permissions)

        self.invitation.is_used = True
        self.invitation.save()

        login(self.request, user)
        return super().form_valid(form)
