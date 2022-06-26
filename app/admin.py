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

    class Media:
        css = {
             'all': ('css/extra_admin.css',)
        }


@admin.register(MonthlyTransaction)
class MonthlyTransactionAdmin(admin.ModelAdmin):
    list_per_page = 100


@admin.register(TransactionGroup)
class TransactionGroupAdmin(admin.ModelAdmin):
    list_per_page = 100


admin.site.enable_nav_sidebar = False
admin.site.site_header = MainAppConfig.verbose_name
