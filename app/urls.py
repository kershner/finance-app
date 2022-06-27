"""finance_by_month URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import HomeView, EditTransactionView, EditTransactionActionView
from django.views.static import serve
from django.urls import path, re_path
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import admin


def custom_error_redirect(request, exception=None):
    return redirect('home')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('edit-transaction', EditTransactionView.as_view(), name='edit-transaction'),
    path('edit-transaction/<transaction_id>', EditTransactionView.as_view(), name='edit-transaction'),
    path('edit-transaction-action', EditTransactionActionView.as_view(), name='edit-transaction-action'),

    # Continue serving static files even with debug = False
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = custom_error_redirect
handler500 = custom_error_redirect
