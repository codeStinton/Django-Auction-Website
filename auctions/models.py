
from django.contrib.auth.models import AbstractUser


from django.db import models

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"


class Auction(models.Model):
    TOYS = 'Toys'
    FASHION = 'Fashion'
    ELECTRONICS = 'Electronics'
    HOME = 'Home'
    OTHER = 'Other'

    CATEGORY = (
        (TOYS, 'Toys'),
        (FASHION, 'Fashion'),
        (HOME, 'Home'),
        (ELECTRONICS, 'Electronics'),
        (OTHER, 'Other'),
    )

  
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4000)
    category = models.CharField(max_length=11, choices=CATEGORY, blank= True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    closed = models.BooleanField(default=False)
    
    image = models.CharField(max_length=255, blank= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'auctionUser')

    create_date = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.id} - {self.title} - {self.user}"

    
class Bids(models.Model):
   
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)

class Comments(models.Model):
    userComment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userComment')
    comment = models.CharField(max_length=255, blank=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.comment} - Auction id: {self.auction.id}"

