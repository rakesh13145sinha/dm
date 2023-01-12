
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
        ("Trial","Trial")
    ]
    MONTHS=[(15,15),(90,90),(180,180),(360,360)]
    subscription=models.CharField(max_length=20,choices=membership)
    days=models.PositiveIntegerField(null=True,choices=MONTHS)
    discount=models.FloatField(null=True)
    price=models.FloatField(null=True)
    status=models.BooleanField(default=True)
    total_access=models.CharField(max_length=10,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=False,auto_now=True)
    recommended=models.CharField(max_length=100,null=True,blank=True)#order to show in ui part
    def __str__(self):
        return self.subscription
    

class PlanFeature(models.Model):
    membership=models.ForeignKey(MemberShip,on_delete=models.CASCADE)
    title=models.CharField(max_length=500)
    image=models.ImageField(upload_to='member/icon')
    priority=models.PositiveIntegerField()
    def __str__(self):
        return self.title
    
    


class Payment(models.Model):
    profile=models.CharField(max_length=50)
    membership=models.CharField(max_length=50)
    status=models.BooleanField(default=False)
    razorpay_order_id=models.CharField(max_length=200)
    razorpay_payment_id=models.CharField(max_length=200)
    razorpay_orderid_signature=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now=False,auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True,auto_now_add=False)