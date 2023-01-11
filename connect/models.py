from django.db import models
from account.models import Person
# Create your models here.

class UpdateRequests(models.Model):
    UPDATE_FILED_REQUEST=[
        ("Food","Food"),
        ("Drink","Drink"),
        ("Star","Star"),
        ("Smoke","Smoke"),                              
        ("Rashi","Rashi"),
        ("Dosham","Dosham")
    ]
    request_status_types = (
    ("Accepted","Accepted"),
    ("Waiting","Waiting"),
    ("Rejected","Rejected"),
    )




    self_profile = models.ForeignKey(Person, on_delete=models.CASCADE,related_name='logged_user')#which person generating request
    other_profile=models.ForeignKey(Person, on_delete=models.CASCADE,related_name='receiver_user')#which person receive this request
    request_status = models.CharField(choices = request_status_types, default="Waiting", max_length = 25)
    update_field_name = models.CharField(choices = UPDATE_FILED_REQUEST, max_length = 25)
    reject_status=models.BooleanField(default=False)#this will true when then person reject one request
    created_date=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated_date=models.DateTimeField(auto_now=False,auto_now_add=True)
    
