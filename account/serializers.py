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


def ViewedPhoneNumberStatus(matrimonyid,requestid):
    
    try:
        view_profile=ViewedPhonNumber.objects.get(profile=matrimonyid)
        check_phone_number=view_profile.view.filter(id=requestid.id)
        if check_phone_number:
            return True
        else:
            return False
    except Exception as e:
        return False




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
        exclude=('user',)


       
class GenderSerializer(serializers.ModelSerializer):
    profileimage=serializers.SerializerMethodField()
    
    def get_profileimage(self,obj):
        images=obj.profilemultiimage_set.all()
        return images[0].files.url if images.exists() else None
    
    
    
    class Meta:
        model=Person 
        fields=['matrimony_id','name',
                'city','state','about_myself',
                'phone_number','occupation',"gender",
                'qualification','caste','country',"active_plan",'dateofbirth','height','profileimage']
        
        
class TabPersonSerializer(serializers.ModelSerializer):
    profileimage=serializers.SerializerMethodField()
    connect_status=serializers.SerializerMethodField()
    album_status=serializers.SerializerMethodField()
    
    
    def get_profileimage(self,obj):
        images=obj.profilemultiimage_set.all()
        return [{"image":image.files.url  if image.files else None } for image in images ] 
    def get_connect_status(self,obj):
        status=connect_status(self.context['matrimony_id'],obj.matrimony_id)
        return status
    
    def get_album_status(self,obj):
       
        try:
            bookmark=Bookmark.objects.get(profile__matrimony_id=self.context['matrimony_id'])
            bookmark.album.get(matrimony_id=obj.matrimony_id)
            return True
        except Exception as e:
            return False
        
                                      
    def to_representation(self, instance):
        representation = super().to_representation(instance)
       
        representation['height'] =instance.height
        representation['phone_status'] =ViewedPhoneNumberStatus(instance.matrimony_id,self.context['matrimony_id'])
        
        return representation                                   
                                
    
    class Meta:
        model=Person 
        fields=['matrimony_id','name',
                'city','state','about_myself','dateofbirth',
                'phone_number','occupation',
                'qualification','caste','country',
                "active_plan","profileimage",'connect_status',"album_status",
                'profile_created_by','dateofbirth',"active_plan"]

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=BannerImage
        fields='__all__'
        
class PPSerializers(serializers.ModelSerializer):
    class Meta:
        model=Partner_Preferences
        fields='__all__'