from .models import CustomUser, MonthlyTransaction, Group
from django.contrib import admin


class MonthlyTransactionInline(admin.TabularInline):
    model = MonthlyTransaction
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_per_page = 100
    inlines = [MonthlyTransactionInline]


@admin.register(MonthlyTransaction)
class MonthlyTransactionAdmin(admin.ModelAdmin):
    list_per_page = 100


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_per_page = 100
