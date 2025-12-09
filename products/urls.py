from django.urls import path
from .views import ProductDetailView, ProductListView, toggle_favorite, BookReadingView


app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_details"),    #!NEED forums.AS_VIEW() BEFORE THIS CAN BE TESTED
    path("<int:pk>/toggle-favorite/", toggle_favorite, name="toggle_favorite"),
    path("<int:pk>/view/", BookReadingView.as_view(), name="book_view"),
]