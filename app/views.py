from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from .forms import MonthlyTransactionForm
from .models import MonthlyTransaction
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from .util import get_user
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
            ctx.update({
                'user': user,
                'net_income_calculations': user.get_net_income_calculations(years_to_project=years)
            })
        return TemplateResponse(request, 'base.html', ctx)


class EditTransactionView(View):
    form = MonthlyTransactionForm()
    template = 'components/includes/edit_transaction_form.html'

    def get(self, request, transaction_id=None):
        if transaction_id:
            transaction = MonthlyTransaction.objects.get(id=transaction_id)
            self.form = MonthlyTransactionForm(instance=transaction)

        ctx = {'form': self.form, 'transaction_id': transaction_id}
        html = render_to_string(self.template, context=ctx, request=request)
        return JsonResponse({'success': True, 'html': html}, status=200)

    def post(self, request, transaction_id=None):
        self.form = MonthlyTransactionForm(request.POST)
        if transaction_id:
            instance = get_object_or_404(MonthlyTransaction, id=transaction_id)
            self.form = MonthlyTransactionForm(request.POST, instance=instance)

        if self.form.is_valid():
            self.form.instance.user = get_user()
            self.form.save()
            # TODO flash message
        else:
            # TODO flash message / handle invalid form
            pass

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
            elif action == 'mute':
                # TODO - implement MUTE functionality
                pass

        except KeyError as e:
            return JsonResponse({'success': False, 'message': 'Incomplete payload, missing: {}'.format(e)})

        return JsonResponse({'success': True}, status=200)
