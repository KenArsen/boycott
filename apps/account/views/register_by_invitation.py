from django.contrib.auth import login
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.account.forms.registration import RegistrationForm
from apps.account.models import Invitation


class RegisterByInvitationView(FormView):
    template_name = "account/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("admin:index")

    def dispatch(self, request, *args, **kwargs):
        """
        Проверяет существование и валидность приглашения.
        """
        try:
            self.invitation = Invitation.objects.get(
                code=kwargs["code"],
                is_used=False,
                expires_at__gt=timezone.now(),  # Проверка срока действия
            )
        except Invitation.DoesNotExist:
            raise Http404(_("Invitation not found, already used, or expired"))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Заполняет начальные данные формы email из приглашения.
        """
        initial = super().get_initial()
        initial["email"] = self.invitation.email
        return initial

    def form_valid(self, form):
        """
        Обрабатывает успешную валидацию формы, создает пользователя и связывает его с приглашением.
        """
        user = form.save(commit=False)
        user.email = self.invitation.email
        user.set_password(form.cleaned_data["password"])

        # Сохраняем пользователя без групп
        user.save()

        # Добавляем пользователя в группу из приглашения
        user.groups.add(self.invitation.group)

        # Устанавливаем права в зависимости от группы
        if self.invitation.group.name == "Moderator":
            user.is_staff = True
        elif self.invitation.group.name == "Admin":
            user.is_staff = True
            user.is_superuser = True
        user.save()

        # Обновляем приглашение
        self.invitation.user = user
        self.invitation.is_used = True
        self.invitation.save()

        # Авторизуем пользователя
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительный контекст для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["invitation"] = self.invitation
        return context
