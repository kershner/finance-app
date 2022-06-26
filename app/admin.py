from .models import CustomUser, MonthlyTransaction, TransactionGroup
from django.contrib import admin
from .apps import MainAppConfig


class MonthlyIncomeTransactionsInline(admin.TabularInline):
    model = MonthlyTransaction
    extra = 0
    verbose_name = 'Monthly Income Transaction'
    verbose_name_plural = 'Monthly Income Transactions'

    def get_queryset(self, request):
        return MonthlyTransaction.objects.filter(user=request.user, type='in').all()


class MonthlyExpenseTransactionsInline(admin.TabularInline):
    model = MonthlyTransaction
    extra = 0
    verbose_name = 'Monthly Expense Transaction'
    verbose_name_plural = 'Monthly Expense Transactions'

    def get_queryset(self, request):
        return MonthlyTransaction.objects.filter(user=request.user, type='ex').all()


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_per_page = 100
    inlines = [MonthlyIncomeTransactionsInline, MonthlyExpenseTransactionsInline]
    fields = ['first_name', 'last_name', 'birth_date', 'starting_value']
    save_on_top = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MonthlyTransaction)
class MonthlyTransactionAdmin(admin.ModelAdmin):
    list_per_page = 100


@admin.register(TransactionGroup)
class TransactionGroupAdmin(admin.ModelAdmin):
    list_per_page = 100


admin.site.site_header = MainAppConfig.verbose_name
