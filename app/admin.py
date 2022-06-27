from .models import CustomUser, MonthlyTransaction, TransactionGroup
from .forms import MonthlyTransactionsInlineForm
from django.contrib import admin
from django.urls import resolve
from .apps import MainAppConfig


class MonthlyIncomeTransactionsInline(admin.TabularInline):
    model = MonthlyTransaction
    extra = 0
    verbose_name = 'Monthly Income Transaction'
    verbose_name_plural = 'Monthly Income Transactions'
    form = MonthlyTransactionsInlineForm

    def get_queryset(self, request):
        return MonthlyTransaction.objects.filter(user=request.user, type='in').all()


class MonthlyExpenseTransactionsInline(admin.TabularInline):
    model = MonthlyTransaction
    extra = 0
    verbose_name = 'Monthly Expense Transaction'
    verbose_name_plural = 'Monthly Expense Transactions'
    form = MonthlyTransactionsInlineForm

    def get_queryset(self, request):
        return MonthlyTransaction.objects.filter(user=request.user, type='ex').all()


class MonthlyTransactionInline(MonthlyIncomeTransactionsInline):
    model = MonthlyTransaction
    extra = 0
    verbose_name = 'Monthly Transaction'
    verbose_name_plural = 'Monthly Transactions'
    form = MonthlyTransactionsInlineForm
    fields = ['type', 'group', 'name', 'amount', 'multiplier', 'muted']
    readonly_fields = ['type']

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.args:
            return self.parent_model.objects.get(pk=resolved.args[0])
        return None

    def get_queryset(self, request):
        parent = self.get_parent_object_from_request(request)
        if parent:
            return MonthlyTransaction.objects.filter(user=request.user, type=parent.type).all()
        return MonthlyTransaction.objects.filter(user=request.user).all()


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_per_page = 100
    inlines = [MonthlyIncomeTransactionsInline, MonthlyExpenseTransactionsInline]
    fields = ['name', 'birth_date', 'starting_value']
    save_on_top = True
    change_form_template = 'admin/custom_change_form.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MonthlyTransaction)
class MonthlyTransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'name', 'group', 'amount', 'multiplier']
    list_display_links = list_display
    list_filter = ['type', 'group']
    sortable_by = list_display
    search_fields = ['name', 'group__group_name']
    save_on_top = True
    fields = ['type', 'name', 'group', 'amount', 'multiplier', 'muted']


@admin.register(TransactionGroup)
class TransactionGroupAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('group_name', 'group_type')
    list_display_links = list_display
    list_filter = ['group_type', 'group_name']
    sortable_by = list_display
    search_fields = ['group_name']
    save_on_top = True
    inlines = [MonthlyTransactionInline]


admin.site.site_header = MainAppConfig.verbose_name
