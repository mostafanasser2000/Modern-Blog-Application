from django.urls import path, include
from . import views
from django.contrib.auth import urls
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("author/<str:username>/", views.profile, name="author"),
    path("login/", views.sign_in, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path(
        "password-change/",
        PasswordChangeView.as_view(template_name="users/password_change_form.html"),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset.html",
            html_email_template_name="users/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
