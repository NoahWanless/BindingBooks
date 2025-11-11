from django.urls import path
from .views import ProdcutDetailView, stripe_config

urlpatterns = [
 
    path("products/<int:product_id>/", ProdcutDetailView.as_view(), name="product_details"),    #!NEED forums.AS_VIEW() BEFORE THIS CAN BE TESTED
    path('config/', stripe_config),
]