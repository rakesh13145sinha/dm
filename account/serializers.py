from rest_framework import serializers
from .models import *
import uuid
from django.contrib.auth.models import User
import string
import random
from age import *
from django.db.models import Q



def connect_status(matrimonyid,requestid):
    # assert matrimonyid is None ,"matrimony id can't be None"
    # assert requestid is None ," requested matrimony id can't be None"
    query=Q(
        Q(profile__matrimony_id=matrimonyid,requested_matrimony_id=requestid)
        |
        Q(profile__matrimony_id=requestid,requested_matrimony_id=matrimonyid)
    )
    send_friend_request=FriendRequests.objects.filter(query)
    if send_friend_request:
        return send_friend_request[0].request_status
    else:
        return "connect"






class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model=Person 
        exclude=("active_plan","total_access",'matrimony_id','user','plan_expiry_date','plan_taken_date')
    
    
    
    
    def create(self, validated_data):
        
        
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
        
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))
                             
        user=User.objects.create(username=str(res)+validated_data['name'])
        return Person.objects.create(user=user,**validated_data)
    
    def update(self, instance, validated_data):
        
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
        fields=['matrimony_id','name',
                'city','state','about_myself',
                'phone_number','occupation',
                'qualification','caste','country',"active_plan"]
        
        
class TabPersonSerializer(serializers.ModelSerializer):
    profileimage=serializers.SerializerMethodField()
    connect_status=serializers.SerializerMethodField()
    
    # response[person.id].update(height_and_age(person.height,person.dateofbirth))
    #         response[person.id].update(connect_status(matrimonyid,person.matrimony_id ) )
    
    def get_profileimage(self,obj):
        images=obj.profilemultiimage_set.all()
        return [{"image":image.files.url  if image.files else None } for image in images ] 
    def get_connect_status(self,obj):
        status=connect_status(self.context['matrimony_id'],obj.matrimony_id)
        return status
                                      
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['age'] =get_age(instance.dateofbirth)
        representation['height'] =height(instance.height)
        # representation['like_status'] = instance.like.filter(id=self.context['userid']).exists()
        # representation['bookmark_status'] = instance.bookmark.filter(id=self.context['userid']).exists()
        # representation['posted_by'] = True if instance.userdetails.id==self.context['userid'] else False
        return representation                                   
                                
    
    class Meta:
        model=Person 
        fields=['matrimony_id','name',
                'city','state','about_myself',
                'phone_number','occupation',
                'qualification','caste','country',"active_plan","profileimage",'connect_status']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=BannerImage
        fields='__all__'
        
class PPSerializers(serializers.ModelSerializer):
    class Meta:
        model=Partner_Preferences
        fields='__all__'