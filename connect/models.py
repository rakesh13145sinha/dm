from django.db import models
from account.models import Person
# Create your models here.

class UpdateRequests(models.Model):
    UPDATE_FILED_REQUEST=[
        ("drinking_habbit","drinking_habbit"),
        ("rashi","rashi"),
        ("star","star"),
        ("smoking_habbit","smoking_habbit"),                              
        ("diet_preference","diet_preference"),
        ("dosham","dosham")
        
    ]
    request_status_types = (
    ("Waiting","Waiting"),
    ("Rejected","Rejected"),
    )

    self_profile = models.ForeignKey(Person, on_delete=models.CASCADE,related_name='logged_user')#which person generating request
    other_profile=models.ForeignKey(Person, on_delete=models.CASCADE,related_name='receiver_user')#which person receive this request
    request_status = models.CharField(choices = request_status_types, default="Waiting", max_length = 25)
    update_field_name = models.CharField(choices = UPDATE_FILED_REQUEST, max_length = 25)
    created_date=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated_date=models.DateTimeField(auto_now=False,auto_now_add=True)
    

class DocumentUpload(models.Model):
    DOC=[('Id','Id'),('Salary_Slip','Salary_Slip'),("Mobile","Mobile"),("Photo","Photo")]
    profile = models.ForeignKey(Person, on_delete=models.CASCADE)
    document=models.ImageField(upload_to='doc/')
    name_of_documunt=models.CharField(max_length=100,choices=DOC)
    status=models.BooleanField(default=False)#after verification it become true
    upload_status=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated_date=models.DateTimeField(auto_now=False,auto_now_add=True)
    
    def __str__(self):
        return self.profile
    
    
    
