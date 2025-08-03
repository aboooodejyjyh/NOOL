from django.urls import path
from .views import PosView

app_name = 'pos'

urlpatterns = [
    path('', PosView.as_view(), name='pos_page'),
]
