from .models import CustomUser, Expense, ExpenseGroup
from django.contrib import admin


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_per_page = 100
    inlines = [ExpenseInline]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_per_page = 100


@admin.register(ExpenseGroup)
class ExpenseGroupAdmin(admin.ModelAdmin):
    list_per_page = 100