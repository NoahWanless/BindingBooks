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
from django.core.mail import send_mail 
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


from products.models import products
from django.contrib.auth import get_user_model
User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    def post(self,request,*args,**kwarfs):
        product = products.objects.get(product_id=self.kwargs["pk"]) #uses the primary key passed in to get the product stuff
        current_user = request.user
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            line_items=[
                {
                    "price_data":{
                        "product":product.product_stripe_id, #this tells stripe what product we are buying in this session
                        "currency":"usd",
                        "unit_amount": int(product.product_price)*100,
                    },
                    "quantity":1,
                }
            ],
            metadata={"product_id":product.product_id,"user_id":current_user.id}, #we'll get this later with
            mode="payment",
            success_url = 'http://127.0.0.1:8000/payments/success/',
            cancel_url = 'http://127.0.0.1:8000/payments/cancel/',

        )
        return redirect(checkout_session.url) #redirects the user to a stripe hosted url that handles all that stuff
    

#this is the view that will get loaded when stripe sends us a payload when it knows whether the 
#transcation has happened or not
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.shortcuts import get_object_or_404

@method_decorator(csrf_exempt,name='dispatch')
class StripeWebhookView(View):
    def post(self,request,format=None):
        payload=request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_KEY
        sig_header=request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload,sig_header,endpoint_secret)
        except ValueError as e:
            #this is if the payload we are sending is invalid
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            #this is if the signature we send is invalid
            return HttpResponse(status=400)
        
        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            session = event["data"]["object"]
            product_id = session["metadata"]["product_id"]
            user_id = session["metadata"]["user_id"]
            print("Here is the product id")
            print(product_id)
            print("Here is the user id")
            print(user_id)
            current_user = get_object_or_404(User, id=user_id)
            #current_user = User.objects.get(id=user_id)
            json_data = current_user.user_owned_books
            json_data.append({'book_id': product_id})
            current_user.user_owned_books = json_data
            current_user.save(update_fields=['user_owned_books'])
            print("We have done everything! yippe")
            

        print("Something happened")

        return HttpResponse(status=200)

