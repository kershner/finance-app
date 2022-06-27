from .forms import MonthlyTransactionForm, AddTransactionGroupForm
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .util import get_user, setup_db_first_time
from django.shortcuts import get_object_or_404
from .models import MonthlyTransaction
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
import json


class HomeView(View):
    @staticmethod
    def get(request):
        min_years = 1
        max_years = 99
        years = int(request.GET.get('years', 1))
        years = int(years if min_years <= years <= max_years else min_years)
        ctx = {
            'years_to_project': years
        }

        user = get_user()
        if user:
            request.session['new_user'] = False

            login(request, user)

            ctx.update({
                'user': user,
                'net_income_calculations': user.get_net_income_calculations(years_to_project=years)
            })
        else:
            request.session['new_user'] = True
            user = setup_db_first_time()
            login(request, user)

            # Redirect to admin page for the user
            return redirect(user.get_admin_url())

        return TemplateResponse(request, 'base.html', ctx)


class EditTransactionView(View):
    transaction_form = MonthlyTransactionForm()
    add_group_form = AddTransactionGroupForm()
    template = 'components/includes/edit_transaction_form.html'

    def get(self, request, transaction_id=None):
        ctx = {}

        if transaction_id:
            transaction = MonthlyTransaction.objects.get(id=transaction_id)
            self.transaction_form = MonthlyTransactionForm(instance=transaction)
            self.add_group_form = AddTransactionGroupForm(instance=transaction.group, initial={'group_name': ''})
            ctx['transaction'] = transaction

        ctx['transaction_form'] = self.transaction_form
        ctx['add_group_form'] = self.add_group_form
        html = render_to_string(self.template, context=ctx, request=request)
        return JsonResponse({'success': True, 'html': html}, status=200)

    def post(self, request, transaction_id=None):
        self.transaction_form = MonthlyTransactionForm(request.POST)
        self.add_group_form = AddTransactionGroupForm(request.POST)

        if transaction_id:
            transaction = get_object_or_404(MonthlyTransaction, id=transaction_id)
            self.transaction_form = MonthlyTransactionForm(request.POST, instance=transaction)

        new_group = None
        if self.add_group_form.is_valid():
            new_group_name = self.add_group_form.cleaned_data['group_name']
            if new_group_name:
                new_group = self.add_group_form.save()
                # TODO flash message

        if self.transaction_form.is_valid():
            self.transaction_form.instance.user = get_user()
            if new_group:
                self.transaction_form.instance.group = new_group
                self.transaction_form.instance.type = new_group.group_type

            self.transaction_form.save()
            # TODO flash message

        return redirect('home')


@method_decorator(csrf_exempt, name='dispatch')
class EditTransactionActionView(View):
    @staticmethod
    def get():
        return JsonResponse({}, status=405)

    @staticmethod
    def post(request):
        try:
            body = json.loads(request.body)
            transaction_id = body['transactionId']
            action = body['action']

            transaction = MonthlyTransaction.objects.get(id=transaction_id)
            if action == 'delete':
                # TODO flash message
                transaction.delete()

        except KeyError as e:
            return JsonResponse({'success': False, 'message': 'Incomplete payload, missing: {}'.format(e)})

        return JsonResponse({'success': True}, status=200)
