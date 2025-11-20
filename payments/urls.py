from django.urls import path
from .views import CancelView, SuccessView, CreateStripeCheckoutSessionView, StripeWebhookView

app_name = "payments"

urlpatterns = [
    
    path("success/<int:ui>/<int:bi>",SuccessView.as_view(),name="success"), #ui = user id, bi = book id (this is for fake checkouts)
    path("success/",SuccessView.as_view(),name="success_default"),
    path("cancel/",SuccessView.as_view(),name="cancel"),


    path("create-checkout-session/<int:pk>/<int:gifted_ui>/", #this will be for gifting, checks before regular session
         CreateStripeCheckoutSessionView.as_view(),
         name="create-checkout-session",
         ),

    path("create-checkout-session/<int:pk>/",
         CreateStripeCheckoutSessionView.as_view(),
         name="create-checkout-session",
         ),
         
    path("webhooks/stripe/",
         StripeWebhookView.as_view(),
         name="stripe-webhook")
]
