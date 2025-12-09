from django.urls import path
from .views import CancelView, SuccessView, CreateStripeCheckoutSessionView, StripeWebhookView,StripeWebhookViewProduction

app_name = "payments"

urlpatterns = [
    #ui = user id, bi = book id (this is for fake checkouts)
    path("success/<int:ui>/<int:bi>",SuccessView.as_view(),name="success"), 
    #this is the real success url
    path("success/",SuccessView.as_view(),name="success_default"),
    path("cancel/",SuccessView.as_view(),name="cancel"),

      #this will be for gifting, checks before regular sessio
    path("create-checkout-session/<int:pk>/<int:gifted_ui>/",
         CreateStripeCheckoutSessionView.as_view(),
         name="create-checkout-session",
         ),

    path("create-checkout-session/<int:pk>/",
         CreateStripeCheckoutSessionView.as_view(),
         name="create-checkout-session",
         ),
         
    path("webhooks/stripe/",
         StripeWebhookView.as_view(),
         name="stripe-webhook"),
     
    path("webhooks/stripe/prod",
         StripeWebhookViewProduction.as_view(),
         name="stripe-webhook-prod")
]
