from .models import EmailConfirm
from django.contrib.auth.models import User
from django.shortcuts import render


def check_permission(original_function):
    def wrapper_function(request, *args, **kwargs):
        try:
            email_confirm = EmailConfirm.objects.get(user=request.user)
            if email_confirm.is_confirmed:
                return original_function(request)
        except TypeError:
            return render(request, "accounts/rejectionPage.html")
    return wrapper_function
