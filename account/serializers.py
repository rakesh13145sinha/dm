from rest_framework import serializers
from .models import *
import uuid
from django.contrib.auth.models import User
class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model=Person 
        exclude=("active_plan","total_access",'matrimony_id','user','plan_expiry_date','plan_taken_date')
    
    def validate(self, data):
        print(data)
        """
        Check name,phone_number,email
        """
        if data['name'] is None or len(data['name'])<3:
            raise serializers.ValidationError("Name is Mandatory Fields")
        
        if len(data['phone_number']) < 10 or 10 < len(data['phone_number']):
            raise serializers.ValidationError("Phone Number should be 10 digit")
        
        if len(data['phone_number']) > 9:
            profile=Person.objects.filter(phone_number=data['phone_number'])
            if profile.exists():
                raise serializers.ValidationError("Phone Number Already In Used")
        
        if data['email']:
            profile=Person.objects.filter(email=data['email'])
            if profile.exists():
                raise serializers.ValidationError("Email Address Already In Used")
        
        
        return data
    
    
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
        
class PPSerializers(serializers.ModelSerializer):
    class Meta:
        model=Partner_Preferences
        fields='__all__'