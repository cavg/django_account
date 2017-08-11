# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Account
from .models import Company

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'company_name')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','identifier', 'address', 'phone')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Account, AccountAdmin)