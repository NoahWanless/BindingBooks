from django.views.generic import DetailView, ListView
from .models import products
from reviews.models import Review
import json
from django.contrib.auth import get_user_model
User = get_user_model()

class ProductListView(ListView):
    model = products
    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = products
    template_name = "product_details.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter( #TODO this line might need to be fixed 
            product_id=self.get_object()
        ).order_by('-review_id')

        current_user_id = self.request.user.id
        current_user = User.objects.get(id=current_user_id)
        display_book = True
        for book in current_user.user_owned_products.all():
            if book.product_id == self.get_object().product_id: #the book in the list is the same book as the one we are trying to purchase
                display_book = False 

        if display_book == False:
            context['display_book'] = False
        else: 
            context['display_book'] = True
        return context







