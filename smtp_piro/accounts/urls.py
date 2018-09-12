from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.information_create_view, name="signup"),
    path('join_success/', views.join_success, name="join_success"),
    path('login/', views.login_view, name="login"),
    path('login_success/', views.login_success, name="login_success"),
    path('logout/', views.logout, name='logout'),

    #이메일인증 smtp
    path('confirm/', views.confirm_email, name='confirm_email'),
    path('confirm/sent/', views.email_confirm_sent, name='email_confirm_sent'),
]
