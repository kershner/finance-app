from django.template.response import TemplateResponse
from .models import CustomUser, Expense, ExpenseGroup
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json


class HomeView(View):
    def get_user(self):
        try:
            return CustomUser.objects.get(id=1)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request):
        years = int(request.GET.get('years', 1))
        years = years if years > 0 else 1

        ctx = {
            'years_to_project': int(years),
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
class UpdateEditFieldsView(View):
    post_values_model_mapping = {
        'user': CustomUser,
        'expense': Expense,
        'expense_group': ExpenseGroup
    }

    def get(self):
        return JsonResponse({}, status=405)

    def post(self, request):
        try:
            body = json.loads(request.body)
            model = body['model']
            instance_id = body['id']
            field = body['field']
            new_value = body['newValue']
        except KeyError as e:
            return JsonResponse({'success': False, 'message': 'Incomplete payload, missing: {}'.format(e)}, status=500)

        return_msg = {'success': True}

        try:
            mapped_model = self.post_values_model_mapping[model]
        except KeyError:
            mapped_model = None

        if mapped_model:
            model_instance = mapped_model.objects.filter(id=instance_id).first()

            # Can only edit User object if it's same user
            no_permissions_msg = {'success': False, 'message': 'You do not have permission to edit this field.'}
            if mapped_model == CustomUser:
                if model_instance != request.user:
                    return JsonResponse(no_permissions_msg, status=403)
            else:
                # Can only edit other objects if they belong to the user
                if hasattr(model_instance, 'user') and model_instance.user != request.user:
                    return JsonResponse(no_permissions_msg, status=403)

            setattr(model_instance, field, new_value)
            model_instance.save()

        return JsonResponse(return_msg, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateCollapseSetting(View):
    def get(self):
        return JsonResponse({}, status=405)

    def post(self, request):
        try:
            body = json.loads(request.body)
            collapse = bool(body['collapse'])
        except KeyError as e:
            return JsonResponse({'success': False, 'message': 'Incomplete payload, missing: {}'.format(e)}, status=500)

        user = request.user
        if not user:
            return JsonResponse({'success': False, 'message': 'Please log in'}, status=403)

        user.collapse_expenses = collapse
        user.save()

        return JsonResponse({'success': True})
