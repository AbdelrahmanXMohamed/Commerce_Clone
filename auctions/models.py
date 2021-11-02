from django.contrib.auth.models import AbstractUser
from django.db import models

'''
    Models:
    Your application should have at least three models in addition to the User model: 
    
        1.for auction listings.
        2.for bids.
        3.for comments made on auction listings. 

    It’s up to you to decide what fields each model should have, 
    and what the types of those fields should be. 
    You may have additional models if you would like.
'''

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Bids(models.Model):

    pass

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time =models.DateTimeField(auto_now=True)
    comments=models.TextField()
    
    def __str__(self):
        return f"{self.id}"
    

class Auctions(models.Model):
    pass    