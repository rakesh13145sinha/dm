
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
    created=models.DateTimeField(auto_now_add=False,auto_now=True)
    def __str__(self):
        return self.subscription