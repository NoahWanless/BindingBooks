from django.urls import path
from .views import ProductDetailView

urlpatterns = [
    path("<int:pk>/", ProductDetailView.as_view(), name="product_details"),    #!NEED forums.AS_VIEW() BEFORE THIS CAN BE TESTED
]