from django.urls import path
from .views import finalize_sale_view

app_name = 'sales'

urlpatterns = [
    path('api/finalize-sale/', finalize_sale_view, name='finalize_sale_api'),
]
