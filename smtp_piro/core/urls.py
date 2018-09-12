from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('byfunc/', views.checkbyFunction, name='byfunc'),
    path('byhtml/', views.checkbyHTML, name='byhtml'),
    path('', views.listofLink, name='base'),
]