from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum_list, name="forum_list"),
    path("<int:forum_id>/", views.forum_detail, name="forum_detail"),
    path("<int:forum_id>/create-post/", views.create_post, name="create_post"),
    path("create/", views.create_forum, name="create_forum"),
    # path("forums/<int:product_id>/", product.as_view(), name="product_details"),    #!NEED PRODUCT.AS_VIEW() BEFORE THIS CAN BE TESTED
]
