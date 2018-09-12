from django.contrib.auth import (authenticate, get_user_model, login, logout as auth_logout, )
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from accounts.forms import LoginForm
from accounts.hash_generator import generate_random_string
from .models import Information, EmailConfirm
from django.contrib.auth.decorators import login_required
from .decorator import check_permission


# Create your views here.
def logout(request):
    auth_logout(request)
    return redirect(reverse("core:base"))


def information_create_view(request):
    if request.method == "POST":
        if request.POST.get('post_type') == 'signup':
            information = Information()
            information.name = request.POST.get('name')
            information.email = request.POST.get('email')
            if information.name is not None:
                user = User.objects.create_user(username=information.email, password=request.POST.get('password'))
                information.user = user
                information.save()
                return redirect('accounts:join_success')
    else:
        return render(request, "accounts/information_create.html")


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                # 이메일인증 smtp
                return login_and_redirect_next(request, user)
            else:
                num = 0
                for person in User.objects.all():
                    if person.username == username:
                        num = num + 1
                if num != 1:
                    login_form.add_error(None, '해당 이메일로 가입된 정보가 없습니다.')
                else:
                    login_form.add_error(None, '비밀번호가 일치하지 않습니다.')
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form,
    }
    return render(request, 'accounts/login.html', context)


def join_success(request):
    return render(request, "accounts/join_success.html")


def login_success(request):
    return render(request, "accounts/login_success.html")


def login_and_redirect_next(request, user):
    if EmailConfirm.objects.filter(user=user, is_confirmed=True).exists():
        login(request, user)
        return redirect(reverse('accounts:login_success'))
    else:
        send_confirm_mail(user)
        return redirect(reverse('accounts:email_confirm_sent'))


def send_confirm_mail(user):
    try:
        email_confirm = EmailConfirm.objects.get(user=user)
    except EmailConfirm.DoesNotExist:
        email_confirm = EmailConfirm.objects.create(
            user=user,
            key=generate_random_string(length=60),
        )

    url = '{0}{1}?key={2}'.format(
        'http://localhost:8000',
        reverse('accounts:confirm_email'),
        email_confirm.key,
    )
    html = '<p>계속하시려면 아래 링크를 눌러주세요.</p><a href="{0}">인증하기</a>'.format(url)
    send_mail(
        '인증 메일입니다.',
        '',
        settings.EMAIL_HOST_USER,
        [user.information.email],
        html_message=html,
    )


def email_confirm_sent(request):
    print("뭐지")
    return render(request, 'accounts/email_confirm_sent.html')


def confirm_email(request):
    key = request.GET.get('key')
    try:
        email_confirm = get_object_or_404(EmailConfirm, key=key, is_confirmed=False)
        email_confirm.is_confirmed = True
        email_confirm.save()
        return redirect(reverse('accounts:login_success'))
    except:
        return render(request, 'accounts/login_fail.html')
