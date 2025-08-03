from django.shortcuts import render
from django.views.generic import TemplateView

class PosView(TemplateView):
    template_name = 'pos/pos_page.html'
