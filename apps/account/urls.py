from django.urls import path

from apps.account.views.register_by_invitation import RegisterByInvitationView

app_name = "account"

urlpatterns = [
    path(
        "register/<uuid:code>/",
        RegisterByInvitationView.as_view(),
        name="registration-with-invite",
    ),
]
