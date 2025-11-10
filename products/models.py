from django.db import models
from django.urls import reverse
from accounts.models import base_user
# Create your models here.


class products(models.Model):
    product_id = models.AutoField(primary_key=True) #primary key
    prodcut_stripe_id = models.TextField(null=False,default='PLACE_HOLDER') #this is where the stripe product id will live fro a product
    prodcut_name = models.TextField(null=False)
    prodcut_link = models.TextField() #^somehow make this so this autogenerates as well
    product_discription = models.TextField()
    product_price = models.FloatField(null=False) #forces a entry to have a price
    prodcut_tags = models.JSONField(default=list) #tags will go here (this is a generic list of any number of items that you might want to put in)
    product_text = models.TextField() #THIS IS WHERE THE ACTUAL BOOK GOES
    product_images = models.JSONField(default=list) #THIS IS WHAT YOU WOULD USE IF YOU HAD IMAGES INSTEAD OF TEXT

    def __str__(self):
        return f"{self.prodcut_name} for: ${self.product_price}"
    
    def get_absolute_url(self):  #! TO BE IMPLEMENTED LATER (when links have been made and stuff)
        return reverse("product_details",kwargs={"product_id":self.product_id})


class product_review(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(base_user,null=True,on_delete=models.SET_NULL)
    product_being_reviewed = models.ForeignKey(products,on_delete=models.CASCADE) #this is so if the product is deleted so is the review (theres nothing to review its gone)
    post_text = models.TextField
    post_reactions = models.JSONField(default=list)
    #star_5_rating = models.IntegerChoices() #! NEED TO DO LATER, OR FIND SOME METHOD THAT DOES THIS 

    def __str__(self):
        return f"{self.author.name} said this: {self.post_text}"