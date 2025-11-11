from django.shortcuts import render



from django.views.generic import TemplateView

class SuccessView(TemplateView):
    template_name = "success.html"#looks in the template file for this html path, and finds it \

class CancelView(TemplateView):
    template_name = "cancel.html"






import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View

from products.models import products

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    def post(self,request,*args,**kwarfs):
        product = products.objects.get(product_id=self.kwargs["pk"]) #uses the primary key passed in to get the product stuff
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            line_items=[
                {
                    "price_data":{
                        "product":product.prodcut_stripe_id, #this tells stripe what product we are buying in this session
                        "currency":"usd",
                        "unit_amount": int(product.product_price)*100,
                    },
                    "quantity":1,
                }
            ],
            metadata={"product_id":product.product_id}, #we'll get this later with
            mode="payment",
            success_url = 'http://127.0.0.1:8000/payments/success/',
            cancel_url = 'http://127.0.0.1:8000/payments/cancel/',

        )
        return redirect(checkout_session.url) #redirects the user to a stripe hosted url that handles all that stuff