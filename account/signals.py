from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Person
from .send_otp import sending_otp
import random
def generate_matrimonyid():
    client=Person.objects.latest("id")
    new_id="DM-2022-"+str(client.user.id)+"-"+str(client.id)
    return new_id


@receiver(post_save, sender=Person)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.matrimony_id=generate_matrimonyid()
        instance.save()
        sending_otp(random.randint(1000,9999), instance.phone_number)