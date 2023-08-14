from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    NameCategory = models.CharField(max_length=42)

    def __str__(self):
        return self.NameCategory

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="biduser")


class Listing(models.Model):
    title = models.CharField(max_length=42)
    description = models.CharField(max_length=420)
    bildUrl = models.CharField(max_length=4242)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="pricebid")
    isON = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="Watchlistitems")

    def __str__(self):
        return self.title

class Comment(models.Model):
     author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentuser")
     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="commentlisting")
     message = models.CharField(max_length=420)

     def __str__(self):
         return f"{self.author} comment on {self.listing}"







    
