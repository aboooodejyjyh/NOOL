from django.urls import path
from .views import ProductListView, ProductCreateView, ProductUpdateView, product_search_view

app_name = 'inventory'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('add/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('api/product-search/', product_search_view, name='product_search_api'),
]
