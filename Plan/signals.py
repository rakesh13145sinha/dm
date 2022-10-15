from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import MemberShip,Payment
from account.models import Person


import random
def generateplanid():
    client=MemberShip.objects.latest("id")
    new_id="DMP-2022-"+str(random.randint(100000,999999))+"-"+str(client.id)
    return new_id

def getmembership(planid):
    client=MemberShip.objects.get(id=planid)
    return client.subscription

@receiver(post_save, sender=MemberShip)
def create_planid(sender, instance, created, **kwargs):
    if created:
        instance.planid=generateplanid()
        instance.save()
        
        
@receiver(post_save, sender=Payment)
def update_profile(sender, instance, created, **kwargs):
    if created:
        person=Person.objects.get(matirmony_id=instance.profile)
        person.active_plan=getmembership(instance.membership)
        person.save()
        instance.save()
        
@receiver(post_delete, sender=Payment)
def delete_payment(sender, instance, **kwargs):
    person=Person.objects.get(matirmony_id=instance.profile)
    person.active_plan="Waiting"
    person.save()
    #instance.save()