from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import products




class ProdcutDetailView(DetailView):
    model = products
    template_name = "product_details.html"
    context_object_name = "product"







