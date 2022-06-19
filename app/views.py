from django.template.response import TemplateResponse


def home(request):
    ctx = {
        'title': 'Poop',
        'message': 'Stinknuggest'
    }
    return TemplateResponse(request, 'base.html', ctx)
