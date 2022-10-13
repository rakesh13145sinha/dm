from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MemberShip

import random
def generateplanid():
    client=MemberShip.objects.latest("id")
    new_id="DMP-2022-"+str(random.randint(100000,999999))+"-"+str(client.id)
    return new_id


@receiver(post_save, sender=MemberShip)
def create_planid(sender, instance, created, **kwargs):
    if created:
        instance.planid=generateplanid()
        instance.save()
        