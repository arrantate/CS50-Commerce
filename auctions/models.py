from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # .listings
    # .watch_list
    # .bids
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, blank=False)
    # .listings

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=60, blank=False)
    description = models.TextField(blank=False)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    date_created = models.DateField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='items_bought')
    image = models.CharField(max_length=500, blank=True)
    seller = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='listings')
    # .bids
    # .watch_list
    
    def __str__(self):
        return self.title


class WatchList(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='watch_list')
    item = models.ForeignKey(Listing, blank=False, on_delete=models.CASCADE, related_name='watch_list')

    def __str__(self):
        return f'{self.user} > {self.item}'


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(Listing, null=False, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return f'{self.date_created.day}-{self.date_created.month}-{self.date_created.year} > {self.bidder} | {self.amount} | {self.listing.title}'
