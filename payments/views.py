from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


#=============================
#SuccessView:
#this view is called when the stripe payment is successful and where the user goes, if we are using a fake purchasing method
#then the user data is sent in the url, and then the model will be updated here
#=============================
class SuccessView(TemplateView):
    template_name = "success.html"#looks in the template file for this html path, and finds it \
    def get(self, request, *args, **kwargs):
        if 'ui' and 'bi' in kwargs:
            ui = self.kwargs["ui"] #user_id
            bi = self.kwargs["bi"] #book_id 
            current_user = get_object_or_404(User, id=ui)
            json_data = current_user.user_owned_books
            json_data.append({'book_id': bi})
            current_user.user_owned_books = json_data
            current_user.save(update_fields=['user_owned_books'])
            print('EVERYTHING WENT FINE, YIPPEE')
        return super().get(request, *args, **kwargs)
    




class CancelView(TemplateView):
    template_name = "cancel.html"






import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.core.mail import send_mail 
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from products.models import products
from django.contrib.auth import get_user_model
User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.shortcuts import get_object_or_404

#=============================
#CreateStripeCheckoutSessionView:
#this view is called when a checkout session is created, takes in the product id and finds the current user
#then creates a stripe checkout session and the user gets taken there, returns metadata found in the 'metadata' var
#'pk' (in the url and hence the kwargs) is the id of the product 
#=============================

class CreateStripeCheckoutSessionView(View):
    def post(self,request,*args,**kwarfs):
        product = products.objects.get(product_id=self.kwargs["pk"]) #uses the primary key passed in to get the product stuff
        #TODO raise error if book doesnt exist 
        #----checks if book is being gifted to a person----#
        if 'gifted_ui' in self.kwargs:
            current_user = User.objects.get(id=self.kwargs["gifted_ui"])
            #TODO raise error if user doesnt exist
        else:
            current_user = request.user

        #----checks if the person who is going to get the product already has it----#
        #TODO
        #TODO
        #TODO
        #TODO
        #----checks if we are doing a fake purchase----#
        if settings.FAKE_STRIPE_PURCHASES == 'True': 
            success_url = request.build_absolute_uri(
                reverse("payments:success", kwargs={"ui": current_user.id, "bi": product.product_id}) #the payments is needed because it is in a namespaced url thingy 
            )
        else: #this is if we are doing real purchases, no user data is sent with the url
            success_url = request.build_absolute_uri(
                reverse("payments:success_default")  
            )

        #----checkout session----#
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
            metadata={"product_id":product.product_id,"user_id":current_user.id}, #we'll get this later after we get a message from stripe
            mode="payment",
            success_url = success_url,
            cancel_url = 'http://127.0.0.1:8000/payments/cancel/',

        )
        return redirect(checkout_session.url) 
    

#=============================
#StripeWebhookView:
#this acts as a listener link, i tell a terminal of mine to send all stripe api messages to the url for this view,
#then it creates the stripe event based on the payload made and depeneding on what event it is, itll do various things
#=============================
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
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        
        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            session = event["data"]["object"]
            product_id = session["metadata"]["product_id"]
            user_id = session["metadata"]["user_id"]
            current_user = get_object_or_404(User, id=user_id)
            json_data = current_user.user_owned_books
            #TODO add it so it checks if the current user already has the book or not 
            #TODO
            #TODO
            json_data.append({'book_id': product_id})
            current_user.user_owned_books = json_data
            current_user.save(update_fields=['user_owned_books'])
            
        return HttpResponse(status=200)


#=============================
#StripeWebhookDeployed:
#this will be the view which is used when a webhook response is sent to the deployed website from stripe, and the model will be updated
#=============================
#TODO
#TODO
#TODO
#TODO