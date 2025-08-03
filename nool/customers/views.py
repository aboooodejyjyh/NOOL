from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Customer

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'customers/customer_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
    success_url = reverse_lazy('customers:customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'customers/customer_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
    success_url = reverse_lazy('customers:customer_list')
