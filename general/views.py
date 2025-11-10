from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView


class HomePageView(TemplateView):
    template_name = "home.html"


