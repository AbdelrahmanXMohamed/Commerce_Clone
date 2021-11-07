from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
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
        return f"Username:{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64,blank=False,null=False)
    def __str__(self):
        return f"{self.name}"
    
    
class Auctions(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE ,null=True)
    name = models.CharField(max_length=64,blank=False,default="not given name")
    imageURL=models.URLField(blank=False,null=True)
    created_at=models.DateTimeField(default=timezone.now)
    description=models.TextField(blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    start_price=models.DecimalField(validators=[MinValueValidator(0.01)],max_digits=7,decimal_places=2,default=0.01)
    current_price=models.DecimalField(validators=[MinValueValidator(0.01)],max_digits=7,decimal_places=2,default=0.01)
    have_bids=models.BooleanField(default=False)
    state=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user} is creating {self.name}"

        

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    auction=models.ForeignKey(Auctions,on_delete=models.CASCADE,null=True)
    time =models.DateTimeField(default=timezone.now)
    comments=models.TextField(blank=False)
    def __str__(self):
        return f"{self.user} is comments {self.auction}"

class Bids(models.Model):
    price=models.DecimalField(max_digits=7,decimal_places=2,default=0)
    winner=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    auction=models.ForeignKey(Auctions,on_delete=models.CASCADE,null=True)
    

    def __str__(self):
        return f"{self.winner} bids on {self.auction} by {self.price}"
class Watchlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    auction=models.ForeignKey(Auctions,on_delete=models.CASCADE,null=True)
