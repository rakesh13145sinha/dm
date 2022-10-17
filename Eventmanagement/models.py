from enum import unique
from django.db import models
from account.models import Person

# Create your models here.
class Vendor(models.Model):
    vendor_name=models.CharField(max_length=100,unique=True)
    image=models.ImageField(upload_to='event/')
    about_vendor=models.TextField()
    status=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=False,auto_now=True)
    
class VentorEvent(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    event_name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='event/')
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    rating=models.CharField(max_length=10,null=True,blank=True)
    price=models.FloatField()
    phone_number=models.CharField(max_length=15)
    status=models.BooleanField(default=True)
    likes=models.ManyToManyField(Person,related_name="likes_by_person")
    category=models.CharField(max_length=100,null=True)
    created_date=models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.envent_name