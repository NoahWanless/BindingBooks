from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse
from products.models import products
from django.contrib.auth import get_user_model
from model_bakery import baker #auto makews the test models
User_model = get_user_model()



class SuccessPageTests(SimpleTestCase):
    def test_url_available_by_name_no_id(self):
        response = self.client.get(reverse("payments:success_default"))
        self.assertEqual(response.status_code,200) 

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/payments/success/") 
        self.assertEqual(response.status_code,200) 

    
    def test_stripe_can_be_accessed(self):
        test_user = baker.make(User_model) 
        test_prodcut = baker.make(products)
        respone = self.client.get('payments:create-checkout-session', pk = test_user.id) #is this method looking in the wrong place?

    
    
class FailurePageTests(SimpleTestCase):
    def test_url_available_by_name(self): 
        response = self.client.get(reverse("payments:cancel"))
        self.assertEqual(response.status_code,200) 

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/payments/cancel/") 
        self.assertEqual(response.status_code,200) 



