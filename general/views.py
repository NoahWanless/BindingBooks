from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView


class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            context["favorites"] = user.favorite_books.all()
        else:
            context["favorites"] = []

        return context
