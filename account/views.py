from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from django.db.models import Q
import random 
from .serializers import *
from .send_otp import *
import os
from age import get_age
from dotenv import load_dotenv
# Create your views here.
load_dotenv('.env')
#print(os.getenv("Phone_nuber_exists_message"))
class Check_Phone_Number(APIView):
    def get(self,request):
        person_phone_number=Person.objects.filter(phone_number__iexact=request.GET['phone_number'])
        if person_phone_number.exists():
            generate_otp=random.randint(1000,9999)
            sending_otp(generate_otp,request.GET['phone_number'])
            return Response({"message":"OTP send successfully",
                             "status":person_phone_number[0].status,
                             "matrimony_id":person_phone_number[0].matrimony_id                             
                             },status=200)
        else:
            return Response({"message":"Accepted",
                            "status":False,
                            "matrimony_id":None                            
                             },status=200)

class Check_Email(APIView):
    def get(self,request):
        person_email=Person.objects.filter(email__iexact=request.GET['email'])
        if person_email.exists():
            return Response({"message":os.environ.get("Email_Exists"),
                            "status":person_email[0].status,
                            "matrimony_id":person_email[0].matrimony_id ,
                             "status":True
                             },status=200)
        else:
            return Response({"message":"Accepted",
                             "status":False ,
                             "status":person_email[0].status,
                            "matrimony_id":person_email[0].matrimony_id                             
                             },status=200)
 

          
class Nation(APIView):
    def get(self,request):
        query=request.GET.get('q')
        response={}
        if query:
            cities=City.objects.filter(state__name=query)
            return Response([{"id":city.id,"name":city.name} for city in cities])    
        else:
            states=State.objects.all()
            return Response([{"id":state.id,"name":state.name} for state in states]) 
                


class Registration(APIView):
    def get(self,request):
        matrimonyid=request.GET.get('matrimony_id')
        if matrimonyid is not None:
            profile=Person.objects.filter(matrimony_id=matrimonyid)
            if profile.exists():
                serializers=ProfileSerializer(profile[0],many=False)
                return Response(serializers.data)
            else:
                return Response({"message":"Invalid Matrimony Id","status":False},status=400)
        else:       
            serializers=ProfileSerializer(Person.objects.all(),many=True)
            return Response(serializers.data)
    
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
           
        data=request.data 
        try:
            phone=data['phone_number']
            email=data['email']
        except KeyError as msg:
            return Response({"message":os.environ.get("Key_Not_Found"),"KeyError":str(msg),"status":False})
        person_phone_number=Person.objects.filter(phone_number__iexact=phone)
        if person_phone_number.exists():
            return Response({"message":os.environ.get("Phone_Number_Exists_Message"),
                             "status":person_phone_number[0].status,
                             "matrimony_id":person_phone_number[0].matrimony_id,
                             "phone_number":person_phone_number[0].phone_number
                             })
        person_email=Person.objects.filter(email__iexact=email)
        if person_email.exists():
            return Response({"message":os.environ.get("Email_Exists"),
                             "status":person_email[0].status,
                            "matrimony_id":person_email[0].matrimony_id,
                             "email":person_email[0].email
                             })
        serializers=PersonSerializers(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":os.environ.get("Profile_Created"),
                             "phone_number":phone
                             })
        else:
            print(serializers.errors)
            return Response(serializers.errors,status=400)
        
    def delete(self,request):
        #matrimonyid=request.GET['matrimony_id']
        person=Person.objects.filter(matrimony_id=request.GET['matrimony_id'])
        if person.exists():
            person.delete()
            
            return Response({"message":"Profile Deleted sucessfully",'status':True})
        else:
            return Response({"message":"Profile Matrimony Id Not Found",'status':False})


"""VALIDATE OTP AUTHENTICATION AND LOGIN WITH OTP""" 
"""api/auth/otp"""
class Validate_OTP(APIView):
    def post(self,request) :
        data=request.data

        try:
           
            data['phone_number']
            data['otp']
            
        except KeyError as msg:
            return Response({"message":str(msg),"status":False,"required_field":True})
        
        
        contactnumber= Person.objects.get(phone_number__iexact=data['phone_number'])    
       
        saved_otp=SaveOTP.objects.get(phone_number__iexact=data['phone_number'])
        
        
        """OTP VARIFICATION """
        if int(data['otp'])==saved_otp.otp:
            
            if data['phone_number'] != "8500001406":
             
                saved_otp.delete()

                contactnumber.status=True

                contactnumber.save()
        
            response={
                "message":"Login successfully",
                "phone_number":contactnumber.phone_number,
                "name":contactnumber.name,
                "matrimony_id":contactnumber.matrimony_id,
                "status":contactnumber.status,
                }
            return Response(response,status=status.HTTP_202_ACCEPTED)
            
        else:
            return Response({"message":"Enter wrong otp","status":False},status=status.HTTP_404_NOT_FOUND)



"""Single Image Post"""
class UploadProfileImage(APIView):
    def get(self,request):
        matrimonyid=request.GET.get('matrimony_id')
        imageid=request.GET.get('imageid')
        response={}
        if imageid is not None:
           
            image=ProfileMultiImage.objects.get(id=imageid)
                
            return Response({                             
                             "image":image.files.url,
                             "imageid":image.id}
                                ,status=200)
           
       
        elif matrimonyid is not None:
            response={}
            profile=Person.objects.get(matrimony_id=matrimonyid)
            uploadedimage=ProfileMultiImage.objects.filter(profile=profile)
            for i in range(6):
                try:
                    response[i+1]={
                        "imageid":uploadedimage[i].id,
                        "image": uploadedimage[i].files.url

                    }
                except Exception as e:
                    response[i+1]={
                        "imageid":None,
                        "image": None,

                    }
                    
                
                
            
            return Response(response.values())
        else:
            return Response({"message":"somethig wrong check and try latter","status":False},status=200)

        


    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
       
        matrimonyid=request.GET['matrimony_id']
        profile=Person.objects.filter(matrimony_id=matrimonyid)
        if profile.exists():
           
            image=ProfileMultiImage.objects.create(
                profile=profile[0],\
                files=request.FILES['image'])
           
            return Response({"message":"Profile Image Uploaded",
                             "status":True,
                             "image":image.files.url,
                             "imageid":image.id},status=200)
        else:
            return Response({"message":"Matrimony Id Invalid",
                             "status":False,
                             "matrimony_id":None},status=400)
       

    def delete(self,request):
        
        imageid=request.GET.get('imageid')
        
        
        image=ProfileMultiImage.objects.filter(id=imageid)
        if image.exists():
            image.delete()
            return Response({"message":"Image successfully Deleted","satus":True},status=203)
        else:
            return Response({"message":"Image Id not Found","status":False},status=404)
        


"""NEW MATCH PROFILE"""
class OppositeGenderProfile(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        person=Person.objects.get(matrimony_id__iexact=matrimonyid)
        query=Q(
            ~Q(gender=person.gender)
            &
            Q(block=False)
            # &
            # Q(reg_date)
            )
        response={}
        persons=Person.objects.filter(query).order_by('-reg_date')[:12]
        for person in persons:
            # serializer=GenderSerializer(person,many=False).data
            # serializer['age']=get_age(person.dateofbirth) 
            images=ProfileMultiImage.objects.filter(profile__id=person.id)
            response[person.id]={
                "image":images[0].image.url if images.exists() else None,
                "matimony_id":person.matrimony_id,
                
            }
        return Response(response.values())
    

"""NEW MATCH JOIN"""
class NewMatchProfile(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        person=Person.objects.get(matrimony_id__iexact=matrimonyid)
        query=Q(
            ~Q(gender=person.gender)
            &
            Q(block=False)
            # &
            # Q(reg_date)
            )
        response={}
        persons=Person.objects.filter(query).order_by('-reg_date')[13:]
        for person in persons:
            images=ProfileMultiImage.objects.filter(profile__id=person.id)
            serializer=GenderSerializer(person,many=False).data
            serializer['image']=images[0].image.url if images.exists() else None
            response[person.id]=serializer
        return Response(response.values())
    
        
