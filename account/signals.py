from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Person,Partner_Preferences
from .send_otp import sending_otp
import random


def create_partner_preferance(pk):
    pp=Person.objects.get(id=pk)
    _,created=Partner_Preferences.objects.get_or_create(profile= pp,min_age= "18",  \
                 max_age= "40",min_height= "4'0'", max_height= "7'0''",  \
                 physical_status= "Does'nt matter", mother_tongue= "Any",  \
                 marital_status= "Does'nt matter", drinking_habbit= "Does'nt matter",  \
                 smoking_habbit= "Does'nt matter",food= "Does'nt matter",  \
                 caste= "Any", religion= "Any",star= "Any",occupation= "Any",  \
                 annual_income= "Any",job_sector= "Any",qualification="Any",  \
                 city= "Any",state= "Any",country= "Any",dosham= "Does'nt matter" ,\
                #description="Good luck !"
                 
                )
    return created


def generate_matrimonyid():
    client=Person.objects.latest("id")
    new_id="DM-2022-"+str(client.user.id)+"-"+str(client.id)
    return new_id


@receiver(post_save, sender=Person)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.matrimony_id=generate_matrimonyid()
        instance.save()
        create_partner_preferance(instance.id)
        sending_otp(random.randint(1000,9999), instance.phone_number)
        


for p in Person.objects.all():
    
    create_partner_preferance(p.id)
# Partner_Preferences.objects.filter(id=1).delete()

#print(Partner_Preferences.objects.values())
