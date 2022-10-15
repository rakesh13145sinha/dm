
from enum import unique
from django.db import models


# Create your models here.

class MemberShip(models.Model):
    membership=[
        ("Platinum","Platinum"),
        ("Silver","Silver"),
        ("Gold","Gold"),
        ("Diamond","Diamond"),
        ("Combo","Combo"),
    ]
    subscription=models.CharField(max_length=20,choices=membership)
    month=models.CharField( max_length=6)
    price=models.CharField(max_length=100)
    message1=models.CharField(max_length=100)
    message2=models.CharField(max_length=100)
    message3=models.CharField(max_length=100)
    message4=models.CharField(max_length=100)
    message5=models.CharField(max_length=100,null=True,blank=True)
    status=models.BooleanField(default=True)
    total_access=models.CharField(max_length=10,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=False,auto_now=True)
    planid=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.subscription
    


class Payment(models.Model):
    profile=models.CharField(max_length=50)
    membership=models.CharField(max_length=50)
    status=models.BooleanField(default=False)
    razorpay_order_id=models.CharField(max_length=200)
    razorpay_payment_id=models.CharField(max_length=200)
    razorpay_orderid_signature=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now=False,auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True,auto_now_add=False)