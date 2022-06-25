from django.contrib.auth.models import AbstractUser
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date
from django.db.models import Sum, F
from django.db import models
from decimal import Decimal
import math


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    starting_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    def get_current_age(self):
        return math.floor((date.today() - self.birth_date).days / 365)

    def get_transactions(self, transaction_type):
        return MonthlyTransaction.objects\
            .filter(user=self, type=transaction_type)\
            .annotate(total=Sum(F('multiplier') * F('amount')))\
            .order_by('-total')\
            .all()

    def get_investments(self):
        return self.get_transactions('ex').filter(group__name='Investment').all()

    def get_transactions_by_group(self, transaction_type):
        transactions_grouped = {}

        transactions = self.get_transactions(transaction_type)
        for transaction in transactions:
            group = transaction.group
            if group not in transactions_grouped:
                transactions_grouped[group] = {
                    'transactions': [transaction],
                    'group_total': group.total()
                }
            else:
                transactions_grouped[group]['transactions'].append(transaction)

        return transactions_grouped

    def get_income_by_group(self):
        return self.get_transactions_by_group('in')

    def get_expenses_by_group(self):
        return self.get_transactions_by_group('ex')

    def get_monthly_transaction_total(self, transaction_type):
        monthly_total = Decimal(0.0)
        all_transactions = self.get_transactions(transaction_type)

        for transaction in all_transactions:
            if not transaction.muted:
                monthly_total += transaction.amount * transaction.multiplier
        return monthly_total

    def get_income_calculations(self):
        total_monthly_income = self.get_monthly_transaction_total('in')
        total_monthly_expenses = self.get_monthly_transaction_total('ex')
        net_monthly_income = total_monthly_income - total_monthly_expenses

        return {
            'total_monthly_income': total_monthly_income,
            'total_monthly_expenses': total_monthly_expenses,
            'net_monthly_income': net_monthly_income
        }

    def get_years_old_from_num_months(self, num_months):
        new_date = date.today() + relativedelta(months=num_months)
        new_delta = new_date - self.birth_date
        return math.floor(new_delta.days / 365)

    def get_net_income_calculations(self, years_to_project=1):
        years_to_project = int(years_to_project)
        now = date.today()
        total_months = years_to_project * 12
        step = int(years_to_project / 1)
        months = range(0, total_months + 1, step)
        income_calcs = self.get_income_calculations()
        total_monthly_investment = self.get_investments().aggregate(Sum('amount'))['amount__sum']

        net_income_calculations = []
        for month in months:
            date_string = (now + timedelta(month * 365 / 12)).strftime('%b %d, %Y')
            net_income = income_calcs['net_monthly_income'] * month
            new_total = self.starting_value + net_income
            new_age = self.get_years_old_from_num_months(num_months=month)
            investment = total_monthly_investment * month
            years_rounded = round(month / 12, 2)
            months_plural = 's' if month != 1 else ''
            time_from_now_string = '{} month{}'.format(month, months_plural)
            years_plural = 's' if years_rounded != 1.00 else ''
            years_string = '{:.2g} year{}'.format(years_rounded, years_plural)
            if month > 12:
                time_from_now_string = years_string

            net_income_calculations.append({
                'time_from_now': time_from_now_string,
                'date_string': date_string,
                'net_income': net_income,
                'new_total': new_total,
                'new_age': new_age,
                'investment': investment
            })

        return net_income_calculations


TRANSACTION_TYPES = [
    ('ex', 'Expense'),
    ('in', 'Income'),
]


class TransactionGroup(models.Model):
    type = models.CharField(max_length=2, choices=TRANSACTION_TYPES, default='ex')
    name = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

    def total(self):
        all_transactions = MonthlyTransaction.objects\
            .filter(group=self, muted=False)\
            .annotate(total=Sum(F('multiplier') * F('amount')))

        total = 0
        for transaction in all_transactions:
            total += transaction.total

        return total


class MonthlyTransaction(models.Model):
    type = models.CharField(max_length=2, choices=TRANSACTION_TYPES, default='ex')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    group = models.ForeignKey(TransactionGroup, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    multiplier = models.IntegerField(default=1)
    muted = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)
