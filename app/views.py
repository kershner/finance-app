from django.template.response import TemplateResponse
from .models import CustomUser, Expense, ExpenseGroup
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json


class HomeView(View):
    def get(self, request):
        return self.common_response(request, years_to_project=1)

    def post(self, request):
        years_to_project = request.POST.get('years')
        return self.common_response(request, years_to_project=years_to_project)

    def common_response(self, request, years_to_project):
        ctx = {
            'years_to_project': int(years_to_project),
            'expense_groups': ExpenseGroup.objects.all()
        }

        user = self.get_user()
        if user:
            ctx.update({
                'user': user,
                'net_income_calculations': user.get_net_income_calculations(years_to_project=years_to_project)
            })
        return TemplateResponse(request, 'base.html', ctx)

    def get_user(self):
        try:
            return CustomUser.objects.get(id=1)
        except CustomUser.DoesNotExist:
            return None


@method_decorator(csrf_exempt, name='dispatch')
class UpdateEditFieldsView(View):
    post_values_model_mapping = {
        'user': CustomUser,
        'expense': Expense
    }

    def get(self):
        return JsonResponse({}, status=405)

    def post(self, request):
        try:
            body = json.loads(request.body)
            print(body)
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
                if model_instance.user != request.user:
                    return JsonResponse(no_permissions_msg, status=403)

            setattr(model_instance, field, new_value)
            model_instance.save()

        return JsonResponse(return_msg, status=200)
