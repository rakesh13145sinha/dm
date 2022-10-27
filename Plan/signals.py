from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import MemberShip,Payment
from account.models import Person
from datetime import timedelta,datetime
from django.db.models import F

import random
def generateplanid():
    client=MemberShip.objects.latest("id")
    new_id="DMP-2022-"+str(random.randint(100000,999999))+"-"+str(client.id)
    return new_id

def getmembership(planid):
    subs=MemberShip.objects.get(id=planid)
    return [subs.subscription,subs.total_access,subs.month]

@receiver(post_save, sender=MemberShip)
def create_planid(sender, instance, created, **kwargs):
    if created:
        instance.planid=generateplanid()
        instance.save()
        
        
@receiver(post_save, sender=Payment)
def update_profile(sender, instance, created, **kwargs):
    if created:
        person=Person.objects.get(matrimony_id=instance.profile)
        plan=getmembership(instance.membership)
        person.active_plan=plan[0]
        person.total_access=F("total_access") + int(plan[1])
        person.plan_taken_date=instance.created_date.date()
        person.plan_expiry_date=instance.created_date.date()+timedelta(days=int(plan[2])*30)
        person.save()
        instance.save()
        
@receiver(post_delete, sender=Payment)
def delete_payment(sender, instance, **kwargs):
    person=Person.objects.get(matrimony_id=instance.profile)
    person.active_plan="Waiting"
    person.total_access=0
    person.save()



    