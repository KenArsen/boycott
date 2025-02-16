import uuid

from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy

from apps.account.forms.invitation import InvitationForm
from apps.account.models import Invitation, User
from apps.account.services import EmailService


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("password", "role")}),
        (
            gettext_lazy("Personal info"),
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                )
            },
        ),
        (
            gettext_lazy("Permissions"),
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
        (gettext_lazy("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_display_links = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("is_active",)
    ordering = ("email",)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "code", "is_used", "created_at")
    form = InvitationForm

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.code = uuid.uuid4()
            obj.save()

            invitation_url = obj.get_invitation_url()
            EmailService.send_email(
                subject="Ваше приглашение для регистрации",
                template_name="account/invitation_send.html",
                recipient_list=[obj.email],
                context={"invitation_url": settings.DOMAIN + invitation_url},
            )
        super().save_model(request, obj, form, change)
