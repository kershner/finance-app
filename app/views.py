from django.template.response import TemplateResponse
from .models import CustomUser, ExpenseGroup
from django.views import View


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
