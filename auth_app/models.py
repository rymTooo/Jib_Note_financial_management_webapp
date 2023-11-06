from django.db import models

# Create your models here.
class signup_model(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    username = models.CharField(max_length=50, primary_key= True)
    password = models.CharField(max_length=50)
    