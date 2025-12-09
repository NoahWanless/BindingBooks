from django.views.generic import DetailView, ListView
from .models import products
from reviews.models import Review
from general.models import Tag
import json
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
User = get_user_model()

class ProductListView(ListView):
    model = products
    template_name = "products/product_list.html"
    context_object_name = "products"
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            # filter by name, description, or tags (tags is JSONField, use icontains for sqlite fallback)
            qs = qs.filter(
                Q(product_name__icontains=q) |
                Q(product_description__icontains=q) |
                Q(product_tags__icontains=q)
            )
        
        # Filter by tag if provided
        tag_id = self.request.GET.get('tag')
        if tag_id:
            qs = qs.filter(product_tags_m2m__pk=tag_id).distinct()
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        context['tags'] = Tag.objects.all().order_by('name')
        return context


class ProductDetailView(DetailView):
    model = products
    template_name = "product_details.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter( #TODO this line might need to be fixed 
            product_id=self.get_object()
        ).order_by('-review_id')

        # Only check owned products for authenticated users. If there is no
        # authenticated user, don't try to query the user model (that would
        # raise DoesNotExist when id is None).
        display_book = True
        request_user = getattr(self.request, 'user', None)
        if request_user and getattr(request_user, 'is_authenticated', False):
            try:
                for book in request_user.user_owned_products.all():
                    if book.product_id == self.get_object().product_id:
                        display_book = False
                        break
            except Exception:
                # If the relationship or user data is malformed, default
                # to showing the purchase button rather than crashing the view.
                display_book = True

        context['display_book'] = display_book
        return context
    

@login_required
def toggle_favorite(request, pk):
    """Add or remove a product from the user's favorites."""
    
    product = get_object_or_404(products, pk=pk)

    # If the user already favorited it → remove it  
    if product in request.user.favorite_books.all():
        request.user.favorite_books.remove(product)
    else:
        request.user.favorite_books.add(product)

    return redirect(request.META.get("HTTP_REFERER", "products:product_list"))

from PyPDF2 import PdfReader

#=================
# View that will display the book to the user
#=================
class BookReadingView(DetailView):
    model = products
    template_name = "read_book.html"
    context_object_name = "product"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #gets the book itself
        request_user = getattr(self.request, 'user', None) #gets current user
        display_book = True #defailt assume the user donesnt have the books #!FOR TESTING ONLY AT THE MOMENT SO I DONT HAVE TO GO AND BUY BOOKS TO VIEW THEM
        if request_user and getattr(request_user, 'is_authenticated', False): 
            try:
                for book in request_user.user_owned_products.all(): #checks if book is in the list
                    if book.product_id == self.get_object().product_id:
                        display_book = True
                        break
            except Exception:
                # If the relationship or user data is malformed, default to not showing the book 
                display_book = False

        context['display_book'] = display_book
        #----------Geting the book text---------#
        reader = PdfReader("static/test_doc.pdf")
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        context['text'] = text

        return context