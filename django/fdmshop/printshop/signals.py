from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import logout
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import redirect


@receiver(user_logged_in)
def prevent_blocked_login(sender, request, user, **kwargs):
    if user.blocat:
        messages.error(request, "Your account is blocked. Please contact an administrator.")
        redirect('login')  # Redirect to the login page
        logout(request)
