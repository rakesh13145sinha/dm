from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
import random 
from .serializers import *
from .send_otp import *
import os
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
                            "status":person_phone_number[0].status,
                            "matrimony_id":person_phone_number[0].matrimony_id                            
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
                             "verify":person_phone_number[0].verify,
                             "block":person_phone_number[0].block
                             })
        person_email=Person.objects.filter(email__iexact=email)
        if person_email.exists():
            return Response({"message":os.environ.get("Email_Exists"),
                             "status":person_email[0].status,
                             "verify":person_email[0].verify,
                             "block":person_email[0].block
                             })
        serializers=PersonSerializers(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":os.environ.get("Profile_Created")})
        else:
            print(serializers.errors)
            return Response(serializers.errors,status=400)
        
    def delete(self,request):
        person=Person.objects.filter(id=request.GET['id'])
        if person.exists():
            person.delete()
            
            return Response({"message":"Profile deleted sucessfully",'status':True})
        else:
            return Response({"message":"Profile Id Not Found",'status':False})
        