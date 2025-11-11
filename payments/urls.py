from django.urls import path
from .views import CancelView, SuccessView, CreateStripeCheckoutSessionView

app_name = "payments"

urlpatterns = [
    path("success/",SuccessView.as_view(),name="success"),
    path("cancel/",SuccessView.as_view(),name="cancel"),
    path("create-checkout-session/<int:pk>/",
         CreateStripeCheckoutSessionView.as_view(),
         name="create-checkout-session",
         ),
]
