from django.urls import path
from .views import ProdcutDetailView

urlpatterns = [
    path("<int:pk>/", ProdcutDetailView.as_view(), name="product_details"),    #!NEED forums.AS_VIEW() BEFORE THIS CAN BE TESTED
]