from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    current_checking_account = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    income_two_weeks = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Expense(models.Model):
    user = models.ForeignKey('app.CustomUser', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(null=False, blank=False, max_length=100)

    EXPENSE_GROUPS = [
        ('UT', 'Utility'),
        ('FO', 'Food'),
        ('MI', 'Misc'),
        ('IN', 'Investment'),
        ('SU', 'Subscription'),
    ]
    group = models.CharField(max_length=2, choices=EXPENSE_GROUPS, default='MI')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
