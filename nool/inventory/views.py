from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Product
from django.http import JsonResponse
from django.db.models import Q

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'inventory/product_form.html'
    fields = ['name', 'barcode', 'price', 'quantity', 'unit', 'reorder_threshold', 'expiration_date']
    success_url = reverse_lazy('inventory:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'inventory/product_form.html'
    fields = ['name', 'barcode', 'price', 'quantity', 'unit', 'reorder_threshold', 'expiration_date']
    success_url = reverse_lazy('inventory:product_list')

def product_search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(barcode__iexact=query)
    )
    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)
