from django.contrib import admin
from .models import CustomUser
from .models import Expense


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_per_page = 100


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_per_page = 100