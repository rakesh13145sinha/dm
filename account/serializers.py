from rest_framework import serializers
from .models import *
import uuid
from django.contrib.auth.models import User
class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model=Person 
        exclude=("active_plan","total_access",'matrimony_id','user')
    def create(self, validated_data):
        user=User.objects.create(username=uuid.uuid4())
        return Person.objects.create(user=user,**validated_data)
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person 
        exclude=('user','image')
        
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person 
        fields=['matrimony_id','name','city','state','about_myself','phone_number','occupation','qualification']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=BannerImage
        fields='__all__'