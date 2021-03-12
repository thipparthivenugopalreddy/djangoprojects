from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    customer=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    profile_pic=models.ImageField(default="")
    phone=models.CharField(max_length=200,null=True,blank=True)
    email=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY=(('Indoor','Indoor'),('Out Door','Out Door'),)
    name=models.CharField(max_length=200,null=True,blank=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tag=models.ManyToManyField(Tag,blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer=models.ForeignKey(Customer,null=True,blank=True,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,null=True,blank=True,on_delete=models.CASCADE)
    STATUS=(('Pending','Pending'),('Out for delivery','Out for delivery'),('Delivered','Delivered'))
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=200,choices=STATUS,null=True,blank=True)
    order_no=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.order_no)
