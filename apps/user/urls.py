from django.urls import path

from apps.user.views.register_by_invitation import RegisterByInvitationView

app_name = "user"

urlpatterns = [
    path(
        "register/<uuid:code>/",
        RegisterByInvitationView.as_view(),
        name="registration-with-invite",
    ),
]
