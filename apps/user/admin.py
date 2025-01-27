import uuid

from django.contrib import admin
from django.utils.translation import gettext_lazy

from apps.user.forms.invitation import InvitationForm
from apps.user.models import Invitation, User
from apps.user.services import EmailService


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
                template_name="user/invitation_send.html",
                recipient_list=[obj.email],
                context={"invitation_url": invitation_url},
            )
        super().save_model(request, obj, form, change)
