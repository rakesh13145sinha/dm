from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Person,Partner_Preferences
from .send_otp import sending_otp
import random
from age import *


def create_partner_preferance(pk):
    pp=Person.objects.get(id=pk)
    _,created=Partner_Preferences.objects.get_or_create(profile= pp,min_age= "18",  \
                 max_age="40",min_height="4'0''", max_height="7'0''",  \
                 physical_status="Any", mother_tongue="Any",  \
                 marital_status="Any", drinking_habbit="Any",  \
                 smoking_habbit="Any",food="Any",  \
                 caste="Any", religion="Any",star="Any",occupation="Any",  \
                 annual_income= "Any",job_sector="Any",qualification="Any",  \
                 city="Any",state="Any",country= "India",dosham="Any" ,\
                description="Good luck !"
                 
                )
    return created


def generate_matrimonyid():
    
    client=Person.objects.latest("id")
    print(client.id)
    # if client.matrimony_id is None:
    #     print(client.matrimony_id)
    #     new_id="DM" +str(int(client.matrimony_id)[2:]+1)
    #     return new_id   
        
    # else:
    #     pattern=102023
    #     new_id="DM"+str(pattern+1)
    #     return new_id
    t=Person.objects.last()
    print(t.id)
    return "DM102023"

@receiver(post_save, sender=Person)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.matrimony_id=generate_matrimonyid()
        instance.dateofbirth=get_age(instance.dateofbirth)
        instance.save()
        sending_otp(random.randint(1000,9999), instance.phone_number)
        create_partner_preferance(instance.id)
        



