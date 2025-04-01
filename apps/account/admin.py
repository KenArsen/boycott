import uuid

from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.account.choices import RoleChoices
from apps.account.forms.invitation import InvitationForm
from apps.account.models import Invitation, User
from apps.account.services import EmailService


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Поля для отображения при редактировании
    fieldsets = (
        (None, {"fields": ("email", "password", "role")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "phone_number")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # Поля для добавления нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role"),
            },
        ),
    )

    # Отображение в списке
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
        "created_at_short",
    )
    list_display_links = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "role")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "last_login")

    # Кастомные методы
    def created_at_short(self, obj):
        """Короткая дата создания"""
        return obj.created_at.strftime("%Y-%m-%d %H:%M") if obj.created_at else "-"

    created_at_short.short_description = _("Created at")

    # Ограничение прав
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_moderator()

    def get_queryset(self, request):
        """Модераторы видят только обычных пользователей"""
        qs = super().get_queryset(request)
        if request.user.is_moderator() and not request.user.is_superuser:
            return qs.exclude(role=RoleChoices.ADMIN)
        return qs


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "role",
        "code_short",
        "is_used",
        "created_at_short",
        "user_link",
    )
    list_filter = ("is_used", "role")
    search_fields = ("email",)
    form = InvitationForm
    actions = ["resend_invitation"]

    # Кастомные методы для отображения
    def code_short(self, obj):
        """Короткий UUID для списка"""
        return str(obj.code)[:8] + "..."

    code_short.short_description = _("Code")

    def created_at_short(self, obj):
        """Короткая дата создания"""
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    created_at_short.short_description = _("Created at")

    def user_link(self, obj):
        """Ссылка на зарегистрированного пользователя"""
        if obj.user:
            url = reverse("admin:account_user_change", args=[obj.user.id])
            return mark_safe(f'<a href="{url}">{obj.user.email}</a>')
        return "-"

    user_link.short_description = _("Registered User")

    # Сохранение и отправка email
    def save_model(self, request, obj, form, change):
        if not change:  # Только при создании
            obj.code = uuid.uuid4()
            super().save_model(request, obj, form, change)
            invitation_url = f"{settings.DOMAIN}{obj.get_invitation_url()}"
            EmailService.send_email(
                subject=_("Your registration invitation"),
                recipient_list=[obj.email],
                template_name="account/invitation_send.html",
                context={"invitation_url": invitation_url, "role": obj.role},
            )
        else:
            super().save_model(request, obj, form, change)

    # Действие для повторной отправки приглашения
    def resend_invitation(self, request, queryset):
        for invitation in queryset.filter(is_used=False):
            invitation_url = f"{settings.DOMAIN}{invitation.get_invitation_url()}"
            EmailService.send_email(
                subject=_("Your registration invitation (resend)"),
                recipient_list=[invitation.email],
                template_name="account/invitation_send.html",
                context={"invitation_url": invitation_url, "role": invitation.role},
            )
        self.message_user(
            request, _(f"Invitations resent to {queryset.count()} users.")
        )

    resend_invitation.short_description = _("Resend selected invitations")

    # Ограничение прав
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_moderator()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
