from .models import CustomUser, MonthlyTransaction, TransactionGroup
from django.contrib import admin


class MonthlyTransactionInline(admin.TabularInline):
    model = MonthlyTransaction
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_per_page = 100
    inlines = [MonthlyTransactionInline]
    fields = ['first_name', 'last_name', 'birth_date', 'starting_value']


@admin.register(MonthlyTransaction)
class MonthlyTransactionAdmin(admin.ModelAdmin):
    list_per_page = 100


@admin.register(TransactionGroup)
class TransactionGroupAdmin(admin.ModelAdmin):
    list_per_page = 100
