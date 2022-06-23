from django.template.response import TemplateResponse
from .models import CustomUser, Expense, ExpenseGroup
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json


class HomeView(View):
    @staticmethod
    def get_user():
        try:
            return CustomUser.objects.get(id=1)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request):
        years = int(request.GET.get('years', 1))
        ctx = {
            'years_to_project': int(years if years > 0 else 1),
            'expense_groups': ExpenseGroup.objects.all(),
        }

        user = self.get_user()
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
    def incomplete_payload_response(e):
        return JsonResponse({'success': False, 'message': 'Incomplete payload, missing: {}'.format(e)}, status=500)


class UpdateEditFieldsView(BasePostResponse):
    post_values_model_mapping = {
        'user': CustomUser,
        'expense': Expense,
        'expense_group': ExpenseGroup
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
            model_instance.save()

        return self.success_response()


class UpdateCollapseSetting(BasePostResponse):
    def post(self, request):
        try:
            body = json.loads(request.body)
            collapse = bool(body['collapse'])
        except KeyError as e:
            return self.incomplete_payload_response(e)

        request.user.collapse_expenses = collapse
        request.user.save()

        return self.success_response()


class AddExpenseView(BasePostResponse):
    @staticmethod
    def post(request):
        new_expense_name = request.POST.get('new-expense-name')
        new_expense_amount = request.POST.get('new-expense-amount')
        expense_group_name = request.POST.get('expense-group-name')

        group, created = ExpenseGroup.objects.get_or_create(name=expense_group_name)
        Expense.objects.get_or_create(
            user=request.user,
            name=new_expense_name,
            amount=new_expense_amount,
            group=group
        )

        # TODO flash message
        return HomeView().get(request)
