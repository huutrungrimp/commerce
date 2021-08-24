from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.urls import reverse
import datetime
from django.utils import timezone



class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=15) 
    slug = models.SlugField(max_length=15, unique=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Listing(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField(null=True)
    slug = models.SlugField(max_length=150, null=False, unique=True)
    listing_pics = models.ImageField(null=True, blank=True, upload_to='images/')
    STATUS = (
        ('ACTIVE', 'Active'),
        ('CLOSE', 'Close'),
        )

    status = models.CharField(
        max_length=6,
        choices=STATUS,
        blank=False,
        default='ACTIVE',
        ) 

    def __str__(self):
        return self.title

    def get_bidprice(self):
        return float(self.price)*1.1


class WatchList(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.listing.title}'


class Bid(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)    
    bidprice = models.FloatField(null=True)
    completed = models.BooleanField(default=False)
    BIDSTATUS = (
        ('WON', 'Won'),
        ('LOST', 'Lost'),
        ('PENDING', 'Pending'),
        )

    bidstatus = models.CharField(
        max_length=8,
        choices=BIDSTATUS,
        blank=False,
        default='PENDING',
        ) 

    
    def __str__(self):
        return f'{self.username}'


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    email = models.EmailField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.username)
