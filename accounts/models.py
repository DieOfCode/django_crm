from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model


class Customer(Model):
    user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default="logo.png",null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ("Indoor", "Indoor"),
        ("Out Door", "Out Door"),

    )
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField(null=True, max_length=200, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out of delivery", "Out of delivery"),
        ('Delivered', "Delivered")
    )
    customer = models.ForeignKey(Customer, null=True,
                                 on_delete=models.SET_NULL)
    products = models.ForeignKey(Product, null=True,
                                 on_delete=models.SET_NULL)

    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.products.name}"
