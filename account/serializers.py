from rest_framework import serializers
from .models import *
import uuid
from django.contrib.auth.models import User
class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model=Person 
        exclude=("active_plan","total_access",'matrimony_id','user','plan_expiry_date','plan_taken_date')
    
    
    
    
    def create(self, validated_data):
        
        print(validated_data)
        """
        Check name,phone_number,email
        """
        if validated_data['name'] is None or len(validated_data['name'])<3:
            raise serializers.ValidationError("Name is Mandatory Fields")
        
        if len(validated_data['phone_number']) < 10 or 10 < len(validated_data['phone_number']):
            raise serializers.ValidationError("Phone Number should be 10 digit")
        
        if len(validated_data['phone_number']) > 9:
            profile=Person.objects.filter(phone_number=validated_data['phone_number'])
            if profile.exists():
                raise serializers.ValidationError("Phone Number Already In Used")
        
        if validated_data['email']:
            profile=Person.objects.filter(email=validated_data['email'])
            if profile.exists():
                raise serializers.ValidationError("Email Address Already In Used")
        
        
        user=User.objects.create(username=uuid.uuid4())
        return Person.objects.create(user=user,**validated_data)
    
    def update(self, instance, validated_data):
        
        print(validated_data)
        """
        update instanse
        """
        
        if  validated_data.get('phone_number'):
            if instance.phone_number !=validated_data.get('phone_number'):
                
                raise serializers.ValidationError("Phone Number can't change")
        
        
        
        if validated_data.get('email'):
            if instance.email != validated_data.get('email'):
                raise serializers.ValidationError("Email Address can't update")
        for key,value in validated_data.items():
            print(getattr(instance,key))
            setattr(instance, key, value)
        
        instance.save()
        return instance
    
    
    
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