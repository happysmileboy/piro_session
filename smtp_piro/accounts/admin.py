from django.contrib import admin
from .models import Information, EmailConfirm


# Register your models here.
@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ['name','email']


admin.site.register(EmailConfirm)