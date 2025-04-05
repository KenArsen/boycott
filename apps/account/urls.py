from django.urls import path

from apps.account.views.authentication import register_view, verify_email_view
from apps.account.views.register_by_invitation import RegisterByInvitationView

app_name = "account"

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", register_view, name="register"),
    path("verify-email/", verify_email_view, name="verify-email"),
    path(
        "register/<uuid:code>/",
        RegisterByInvitationView.as_view(),
        name="registration-with-invite",
    ),
]
