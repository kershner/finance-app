from .models import CustomUser, MonthlyTransaction, Group
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
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
            'years_to_project': years,
            'income_groups': Group.objects.filter(type='in').all(),
            'expense_groups': Group.objects.filter(type='ex').all(),
        }

        user = get_user()
        if user:
            ctx.update({
                'user': user,
                'net_income_calculations': user.get_net_income_calculations(years_to_project=years)
            })
        return TemplateResponse(request, 'base.html', ctx)


@method_decorator(csrf_exempt, name='dispatch')
class BasePostResponse(View):
    @staticmethod
    def get():
        return JsonResponse({}, status=405)

    @staticmethod
    def success_response():
        return JsonResponse({'success': True}, status=200)

    @staticmethod
    def error_response(msg):
        return JsonResponse({'success': False, 'message': msg}, status=500)

    def incomplete_payload_response(self, e):
        return self.error_response('Incomplete payload, missing: {}'.format(e))


class UpdateEditFieldsView(BasePostResponse):
    post_values_model_mapping = {
        'user': CustomUser,
        'monthly_transaction': MonthlyTransaction,
        'group': Group
    }

    def post(self, request):
        try:
            body = json.loads(request.body)
            model = body['model']
            instance_id = body['id']
            field = body['field']
            new_value = body['newValue']
        except KeyError as e:
            return self.incomplete_payload_response(e)

        try:
            mapped_model = self.post_values_model_mapping[model]
        except KeyError:
            mapped_model = None

        if mapped_model:
            model_instance = mapped_model.objects.filter(id=instance_id).first()
            setattr(model_instance, field, new_value)

            try:
                model_instance.save()
            except (ValidationError, ValueError) as e:
                return self.error_response(e.message if hasattr(e, 'message') else str(e))

        return self.success_response()


class AddTransactionView(BasePostResponse):
    @staticmethod
    def post(request):
        new_transaction_type = request.POST.get('new-transaction-type')
        new_transaction_name = request.POST.get('new-transaction-name')
        new_transaction_amount = request.POST.get('new-transaction-amount')
        group_name = request.POST.get('transaction-group-name')

        group, created = Group.objects.get_or_create(name=group_name, type=new_transaction_type)
        MonthlyTransaction.objects.get_or_create(
            user=get_user(),
            type=new_transaction_type,
            name=new_transaction_name,
            amount=new_transaction_amount,
            group=group
        )

        # TODO flash message
        return HomeView().get(request)
