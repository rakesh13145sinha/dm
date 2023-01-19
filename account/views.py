import os
import random
# from datetime import datetime ,date,timedelta

import pytz 
from decouple import config
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from itertools import chain
from age import *

from .models import *
from .send_otp import *
from .serializers import *
from connect.status import *
from record import *

print("This is testing phase. Don't mind it.................")


def connection(**kwargs):
    return kwargs
"""UPLOAD BANNER IMAGE"""
class Banner(APIView):
    def get(self,request):
        serializers=BannerSerializer(BannerImage.objects.all())
        return Response(serializers.data)
    def post(self,request):
        data=request.data 
        serializers=BannerSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors)
    
    def put(self,request):
        data=request.data 
        bannerid=request.GET['id']
        banner=BannerImage.objects.get(id=bannerid)
        serializers=BannerSerializer(banner,data=data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors)
        
    def delete(self,request):
        bannerid=request.GET['id']
        try:
            BannerImage.objects.get(id=bannerid).delete() 
        except Exception as e:
            return Response({"message":"Banner deleted"}) 


"""This function for  view profile check"""
def ViewedProfiles(matrimonyid,requestid,status=None):
    """self matrimony id"""
    selfprofile=get_object_or_404(Person,matrimony_id=matrimonyid)
    
    """requested matrimony id"""
    requested_profile=get_object_or_404(Person,matrimony_id=requestid)
    
    view_profile=ViewedProfile.objects.filter(profile__id=selfprofile.id)
    if status is None:                  
        if view_profile.exists():
            if view_profile[0].view.filter(id=requested_profile.id).exists():
                pass
            else:
                view_profile[0].view.add(requested_profile)
        else:
            
            view_profile=ViewedProfile.objects.create(profile=selfprofile)
            view_profile.view.add(requested_profile)
        return True
    elif status is not None:
        if view_profile.exists():
            return view_profile[0].view.filter(id=requested_profile.id).exists()
        else:
            return False







"""VIEW PHONE NUMBERS"""
"""This function for  view profile check"""
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
   

"""check request status"""       
def connect_status(matrimonyid,requestid):
    # assert matrimonyid is None ,"matrimony id can't be None"
    # assert requestid is None ," requested matrimony id can't be None"
    query=Q(
        Q(profile__matrimony_id=matrimonyid,requested_matrimony_id=requestid)
        |
        Q(profile__matrimony_id=requestid,requested_matrimony_id=matrimonyid)
    )
    send_friend_request=FriendRequests.objects.filter(query)
    if send_friend_request.exists():
        return {"connect_status":send_friend_request[0].request_status} 
    else:
        return {"connect_status":"connect"}   
        
def height_and_age(h,age=None):
   
    if h is not None:
        return {'height':height(h)}   
    
    elif h is None:
        return {'height':None}




def mutual_match(matrimony_id):
        response = {}
        main_user = Person.objects.filter(matrimony_id=matrimony_id).values()
        partner_user = Person.objects.filter(~Q(gender=main_user[0]["gender"])).values()
        for index , keys in enumerate(partner_user):
            response[index]={"id":keys['id']}
            _list=['user_id' ,'id','plan_taken_date',
                   'plan_expiry_date','reg_date','reg_update' ,'total_access',
                   'active_plan','verify' , 'block',  'gender' ,'phone_number','name' ,
                   'status','about_myself','matrimony_id','email']
            for i in _list:
                del keys[i]
            user_full_details= dict(ChainMap(*[{k : True} if partner_user[index][k] == main_user[0][k] else {k:False} for k,v in keys.items()]))
            
            response[index].update(user_full_details)
        matrimonyid=[{"id":value['id'],"count":len([j for i, j in value.items() if j == True])} for key,value in response.items()]
        
        sorted_list=sorted(matrimonyid,key=lambda x:x['count'],reverse=True)
        
        list_of_id=[ i['id'] for i in sorted_list]
        return list_of_id


class Check_Phone_Number(APIView):
    def get(self,request):
        try:
            phone=request.GET['phone_number']
        except KeyError as e:
            return Response({"message":"Phone number is mandatory key","error":str(e)})
        try:   
            person_phone_number=Person.objects.get(phone_number__iexact=phone)
        except Exception as e:
            return Response({"message":"Accepted",
                            "status":False,
                            "matrimony_id":None                            
                             },status=200)
        
        #only testing purpose only
        if phone=="8500001406":
            SaveOTP.objects.get_or_create(phone_number=phone,otp=1406)
            return Response({"message":"Testing purpose only",
                            "status":person_phone_number.status,
                            "matrimony_id":person_phone_number.matrimony_id                             
                            },status=200)
        else:   
            generate_otp=random.randint(1000,9999)
            sending_otp(generate_otp,phone)
            return Response({"message":"OTP send successfully",
                            "status":person_phone_number.status,
                            "matrimony_id":person_phone_number.matrimony_id                             
                            },status=200)
       

class Check_Email(APIView):
    def get(self,request):
        person_email=Person.objects.filter(email__iexact=request.GET['email'])
        if person_email.exists():
            return Response({"message":config("Email_Exists"),
                            "status":person_email[0].status,
                            "matrimony_id":person_email[0].matrimony_id ,
                             
                             },status=200)
        else:
            return Response({"message":"Accepted",
                             "status":False ,
                            "matrimony_id":None                            
                             },status=200)
 

          
class Nation(APIView):
    def get(self,request):
        query=request.GET.get('q')
        response={}
        if query is not None:
            # cities=City.objects.filter(state__name=query)
            if query=="Telangana":
                return Response([{"name":city} for city in telangana]) 
            elif query=="Andhra Pradesh": 
                return Response([{"name":city} for city in andhara])
            else:
                return Response([])  
        else:
            return Response([{"name":state} for state in states]) 


########################PROFILE API#################################               
"""Single Profile get"""
class SingleProfile(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        requestid=request.GET['requeted_matrimony_id']
       
        self_profile=Person.objects.filter(matrimony_id=matrimonyid).only('matrimony_id')
        if self_profile:
            #getting self these field for updated or not if not update then update
            user_profile=self_profile.values('drinking_habbit','rashi','star','dosham',\
                                             'smoking_habbit','diet_preference')
        else:
            return Response({"message":"Invalid matrimony_id"},status=200)
        
        try:
            profile=Person.objects.get(matrimony_id=requestid)
        except Exception as e:
            return Response({"message":"Invalid requested matrimony id"},status=400)
       
        images=profile.profilemultiimage_set.all()
        
        #bookmark
        bookmark=Bookmark.objects.filter(profile__matrimony_id=matrimonyid,album__matrimony_id=requestid)
        #view profile
        ViewedProfiles(matrimonyid,requestid)
        #check phone number views statas
        phone_status=ViewedPhoneNumberStatus(self_profile[0],profile)
    
        serializers=ProfileSerializer(profile,many=False).data
        serializers['profileimage']=[
            {"id":image.id,"image":image.files.url if image.files else None}
            for image in images ]
        serializers['phone_status']= phone_status
        serializers['bookmark']= True if bookmark.exists() else False
        serializers['self_profile']=user_profile[0] 
        list_of_field=[key for key in user_profile[0].keys()  ]
        serializers['request_status']=request_status(self_profile[0],profile,list_of_field) 
        serializers.update(connect_status(matrimonyid,requestid))
        
        return Response(serializers)
        
       
"""Registration for new user"""
class Registration(APIView):
    
    def get(self,request):
        matrimonyid=request.GET.get('matrimony_id')
        if matrimonyid is not None:
            try:
                profile=Person.objects.get(matrimony_id=matrimonyid)
            except Exception as e:
                return Response({"message":"Invalid matrimony id"},status=400)
            images=profile.profilemultiimage_set.all()
            serializers=ProfileSerializer(profile,many=False).data
            serializers['profileimage']=[
                {"id":image.id,"image":image.files.url if image.files else None}
                for image in images ]
            
            return Response(serializers)
            
        else: 
            profiles=Person.objects.all().order_by("-id")
            response={}
            for profile in profiles:
                images=ProfileMultiImage.objects.filter(profile__id=profile.id)
                serializers=ProfileSerializer(profile,many=False).data
                serializers['profileimage']=[
                    {"id":image.id,"image":image.files.url if image.files else None}
                    for image in images ]
                # serializers.update(height_and_age( profile.height,profile.dateofbirth ))
                response[profile.id]=serializers
            return Response(response.values())
    
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
           
        data=request.data 

        serializers=PersonSerializers(data=data)
        print(data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":config("Profile_Created"),
                             "phone_number":data['phone_number']
                             })
        else:
            print(serializers.errors)
            return Response(serializers.errors,status=400)
    
    def put(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True 
        data=request.data 
        person=Person.objects.get(matrimony_id=request.GET['matrimony_id'])
        serializers=PersonSerializers(person,data=data,partial=True)
        data['user']=person.user.id
        if serializers.is_valid():
            serializers.save()
            get_fields=Person.objects.filter(id=person.id)\
           .values('drinking_habbit','rashi','star','dosham',\
                                             'smoking_habbit','diet_preference')
            updated_field=[key for key,value in get_fields[0].items() if value is not None]
            delete_request(person,updated_field)
            return Response({"message":"Profile Updated successfully",
                             
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
        images=ProfileMultiImage.objects.filter(profile=contactnumber)
        
        """OTP VARIFICATION """
        if int(data['otp'])==saved_otp.otp:

            saved_otp.delete()

            contactnumber.status=True

            contactnumber.save()
        
            response={
                "message":"Login successfully",
                "phone_number":contactnumber.phone_number,
                "name":contactnumber.name,
                "matrimony_id":contactnumber.matrimony_id,
                "image":images[0].files.url if images.exists() else None,
                "status":contactnumber.status,
                "active_plan":contactnumber.active_plan,
               
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
    
    
    def put(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
       
        image=ProfileMultiImage.objects.get(id=request.GET['imageid'])
        
        image.files=request.FILES['image']
        image.save()  
        return Response({"message":"Profile Image Updated Successfully",
                            "status":True,
                            "image":image.files.url,
                            "imageid":image.id},status=200)
        

    def delete(self,request):
        
        imageid=request.GET.get('imageid')
        
        
        image=ProfileMultiImage.objects.filter(id=imageid)
        if image.exists():
            image.delete()
            return Response({"message":"Image successfully Deleted","satus":True},status=203)
        else:
            return Response({"message":"Image Id not Found","status":False},status=404)
        

#################################END###############################

"""NEW MATCH PROFILE"""
class OppositeGenderProfile(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        person=Person.objects.get(matrimony_id__iexact=matrimonyid)
        query=Q(
           ~ Q(gender=person.gender)
            &
            Q(block=False)
           
            )
        
        persons=Person.objects.filter(query).order_by('-reg_date')[0:12]
        
       
        data=[{
            "image":person.profilemultiimage_set.all()[0].files.url if person.profilemultiimage_set.all() else None,
            "matimony_id":person.matrimony_id,
            "name":person.name,
            "occupation":person.occupation,
            "qualification":person.qualification,
            "city":person.city,
            "state":person.state,
            "country":person.country,
            "caste":person.caste,
            "dateofbirth":person.dateofbirth,
            "height":person.height
            }
            for person in persons
            ]
        return Response({"message":"success","data":data})
    








"""BOOKMARK MATRIMONY ID"""

########################BOOKMARK API START#######################
class BookMarkProfile(APIView):
    def get(self,request) :
        matrimonyid=request.GET['matrimony_id']
        requestid=request.GET['requeted_matrimony_id']
        
        
        try:
            selfid=Person.objects.get(matrimony_id=matrimonyid)
        except Exception as e:
            return Response({"message":"Invalid  matrimony id"},status=400)
        
        try:
            profile=Person.objects.get(matrimony_id=requestid)
        except Exception as e:
            return Response({"message":"Invalid requested matrimony id"},status=400)
        
        
        try:
            bookmark=Bookmark.objects.get(profile=selfid) 
            if bookmark.album.filter(matrimony_id=requestid):
                bookmark.album.remove(profile)
            
                return Response({"bookmark":False,"status":False})
            else:
                bookmark.album.add(profile)
                return Response({"bookmark":True,"status":True})
        except Exception as e:
            bookmark=Bookmark.objects.create(profile=selfid)
            bookmark.album.add(profile)
            return Response({"bookmark":True,"status":True})
       

class Album(APIView):
    def get(self,request) :
        matrimonyid=request.GET['matrimony_id']
        bookmark=Bookmark.objects.select_related("profile")\
        .filter(profile__matrimony_id=matrimonyid)   
        if bookmark.exists():
            response={}
            bookmarks=bookmark[0].album.all()
            for person in bookmarks:
                images=ProfileMultiImage.objects.filter(profile__id=person.id)
                response[person.id]={
                    "profileimage":images[0].files.url if images.exists() else None,
                    "matrimony_id":person.matrimony_id
                    }
                                        
            return Response(response.values())
           
                
        else:
            return Response([],status=200)
       
########################BOOKMARK API START#######################            
        

@api_view(['GET'])
def profile_match_percentage(request):
    matrimonyid=request.GET['matrimony_id']
    requestid=request.GET['requeted_matrimony_id']
    try:
        profile=Person.objects.get(matrimony_id=matrimonyid)
    except Exception as e:
        return Response({"message":"Invalid matrimony id","error":str(e)},status=400)
    try:
        target_profile=Person.objects.get(matrimony_id=requestid)
    except Exception as e:
        return Response({"message":"Invalid  requested matrimony id","error":str(e)},status=400)
    
    
    
    #my preference
    pp=Partner_Preferences.objects.get(profile=target_profile)
    
    _height_list=[
    "3'1''","3'2''","3'3''","3'4''","3'5''","3'6''","3'7''","3'8''","3'9''","3'10''","3'11''","4'0''" , 
    "4'1''","4'2''","4'3''","4'4''","4'5''","4'6''","4'7''","4'8''","4'9''","4'10''","4'11''","5'0''" , 
    "5'1''","5'2''","5'3''","5'4''","5'5''","5'6''","5'7''","5'8''","5'9''","5'10''","5'11''","6'0''",
    "6'1''","6'2''","6'3''","6'4''","6'5''","6'6''","6'7''","6'8''","6'9''","6'10''","6'11''","7'0''",
    "7'1''","7'2''","7'3''","7'4''","7'5''","7'6''","7'7''","7'8''","7'9''","7'10''","7'11''","8'0''"
        
        ]
    
    _index={"min_height":_height_list.index(pp.min_height),"max_height":_height_list.index(pp.max_height)}
    
    target_profile_index=_height_list.index(profile.height)
    
    response={
        "dateofbirth":True if  int(profile.dateofbirth) in range(int(pp.min_age),int(pp.max_age)) else False,
        "height":True if target_profile_index in range(_index['min_height'],_index['max_height']) else False,
        'physical_status': True if pp.physical_status=="Any" or  pp.physical_status== profile.physical_status else False,
        
        'mother_tongue': True if pp.mother_tongue=="Any" or pp.mother_tongue==profile.mother_tongue else False,
        "marital_status": True if  pp.marital_status=="Any" or pp.marital_status==profile.marital_status else False,
        'religion': True if (pp.religion=="Any" or pp.religion==profile.religion) else False,
        
        
        'occupation': True if pp.occupation=="Any" or pp.occupation==profile.occupation else False,
        "annual_income": True if pp.annual_income=="Any" or pp.annual_income==profile.annual_income else False,
        'country': True if pp.country=="Any" or pp.country==profile.country else False,
        
        
        "qualification":True if pp.qualification=="Any" or pp.qualification==profile.qualification else False,
        
        }  
    
    my_preference={
        "age_range":pp.min_age+"-"+pp.max_age ,
        "height_range":pp.min_height+" "+"-"+" "+pp.max_height,
        "physical_range":pp.physical_status,
        
        "mother_tongue_range":pp.mother_tongue,
        "marital_range":pp.marital_status,
        "religion_range":pp.religion,
        
        "occupation_range":pp.occupation,
        "annual_income_range":pp.annual_income,
        "country_range":pp.country,
        "qualification_range":pp.qualification
        
        
        }
    
    matched_field=sum([1 for value in response.values() if value is True ])
    not_match_filed=sum([1 for value in response.values() if value is False ])
    
    
    number_of_fields=matched_field+not_match_filed
    try:
        updated_code=(matched_field*100)//number_of_fields
    except ZeroDivisionError:
        updated_code=0
    response.update(my_preference)
    response.update({"percentage":updated_code})
    
    return Response(response,status=200)








       



"""HOW MUCH PROFILE UPDATED IN PERCENTAGE"""       
class ProfileUpdatePercentage(APIView):
    def get(self,request):
        import json
        matrimonyid=request.GET['matrimony_id']
        change_into_dict = Person.objects.filter(matrimony_id=matrimonyid).values()[0]
        
        _list=['user_id' ,'id','reg_date','reg_update','plan_taken_date','plan_expiry_date' ,
               'total_access','active_plan','verify' , 'block',  'gender' ,'phone_number','name' ,
               'status','matrimony_id']
        for i in _list:
            del change_into_dict[i]
        count=len( list (filter(lambda x:x!=None,change_into_dict.values())))
        percentage=(count*100)//len(change_into_dict) 
        
        images=ProfileMultiImage.objects.select_related('profile').filter(profile__matrimony_id=matrimonyid)
        data={
            "profileimage":images[0].files.url if images.exists() else None,
            "matrimony_id":matrimonyid,
            "percentage":percentage
        }            
        return Response(data)
        


      


class DailyRecomandation(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        profile=Person.objects.get(matrimony_id=matrimonyid)
        query=Q(
           Q(   ~Q(gender=profile.gender)
                &
                Q(status=True)
            )
           &
           Q(
               Q(physical_status=profile.physical_status)
               |
               Q(mother_tongue=profile.mother_tongue)
               |
               Q(marital_status=profile.marital_status)
               |
               Q(drinking_habbit=profile.drinking_habbit)
               |
               Q(smoking_habbit=profile.smoking_habbit)
               |
               Q(diet_preference=profile.diet_preference)
               |
               Q(caste=profile.caste)
               |
               Q(religion=profile.religion)
               |
               Q(occupation=profile.occupation)
               |
               Q(job_sector=profile.job_sector)
               |
               Q(smoking_habbit=profile.smoking_habbit)
               |
               Q(city=profile.city)
               |
               Q(state=profile.state)
               |
               Q(religion=profile.religion)
               |
               Q(occupation=profile.occupation)
               |
               Q(qualification=profile.qualification)

           ) 
           
            
        )
        
        response={}
        r_profile=Person.objects.filter(query).order_by('-reg_date')
        for r_pro in r_profile:
            images=r_pro.profilemultiimage_set.all()
            response[r_pro.id]={
                "matrimony_id":r_pro.matrimony_id,
                "image":images[0].files.url if images.exists() else None,
                "height":height(r_pro.height),
                "dateofbirth":r_pro.dateofbirth,
                "gender":r_pro.gender,
                "name":r_pro.name,
                "phone_number":r_pro.phone_number
                
            }
            response[r_pro.id].update(connect_status(matrimonyid,r_pro.matrimony_id))
        
        return Response(response.values(),status=200)
    
    


"""SHFFLEING PROFILE SHOWING OPPISITE GENDER PROFILE"""
class NeedToUpdateFields(APIView):
    def get(self,request):
        response={}
        matrimonyid=request.GET['matrimony_id']
        
        profile=Person.objects.get(matrimony_id=matrimonyid)
        
        _list=['horoscope',"habbits",'workplace','star',
               "total_family_members",'college' ,"annual_income"]
        
        
        for info in _list:
            if getattr(profile,info)=="" or getattr(profile,info) is None :
                
                response[info]={ 
                                "name":info,
                                "about":"Get 90 imes more boostup your profile"
                                }                             
            else:
                pass                   
            images=ProfileMultiImage.objects.filter(profile__matrimony_id=matrimonyid)
            if images.exists()==False:
                response['image']={
                "name":"image",
                "about":"Get 90 imes more boostup your profile"
                }                     
        return Response(response.values())
    


"""Explore"""
class Explore(APIView):
    def get(self,request):
        
        matrimonyid=request.GET['matrimony_id']
        
        profile=Person.objects.get(matrimony_id=matrimonyid)
        
        profile=Person.objects.aggregate(
            star=Count('pk', filter=Q(
                Q(star=profile.star)& ~Q(gender=profile.gender)
                )),
            occupation=Count('pk', filter=Q(
                
                Q(occupation=profile.occupation)& ~Q(gender=profile.gender)
                )),
            qualification=Count('pk', filter=Q(
                
                Q(qualification=profile.qualification)& ~Q(gender=profile.gender)
                )),
            
            # horoscope=Count('pk', filter=Q(
                
            #     Q(horoscope=profile.horoscope)& ~Q(gender=profile.gender)
            #     )),
           
            city=Count('pk', filter=Q(
                
                Q(city=profile.city)& ~Q(gender=profile.gender)
                )),
            
            
           
        
        )   
        response={}
        for key,value in profile.items():
            banner=BannerImage.objects.filter(name=key,status=True)
            response[key]={
                "name":key,
                "image":banner[0].image.url if banner else None,
                "color":banner[0].background if banner else None,
                "count":value
            }            
        return Response(response.values())
    

 
 

#######################FRIEND REQUEST SEND#########################    
"""SEND FRIEND REQUEST"""   
class SendFriendRequest(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        requestid=request.GET['requeted_matrimony_id']
        query=Q(
            profile__matrimony_id=matrimonyid,
            requested_matrimony_id=requestid,
            status=True
        )
        try:
            sender=Person.objects.get(matrimony_id=matrimonyid)
        except Exception as e:
            return Response({"message":"Invalid matrimony id","error":str(e)},status=400)
        
        try:
            receiver=Person.objects.get(matrimony_id=requestid)
           
        except Exception as e:
            return Response({"message":"Invalid matrimony id","error":str(e)},status=400)
        if sender.gender==receiver.gender:
            return Response({"message":"Both id belongs to same gender","error":str(e)},status=400)
        
        try:
            send_friend_request=FriendRequests.objects.get(query)
            return Response({"message":"Request Exsits",
                             "connect_status":send_friend_request.request_status})
        except Exception as e:
            sender.friendrequests_set.create(requested_matrimony_id=receiver.matrimony_id,status=True)
            return Response({"message":"Request Send Successfully","connect_status":"Waiting"},status=200)
    
    
       
    def put(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
        data=request.data
        connectid=request.GET['connectid']
        _list=("Connected","Rejected")
        if data['request_status'] not in _list:
            return Response({"message":"Invalid Choice","status":False},status=400)
        
        
        get_request=FriendRequests.objects.get(id=connectid)
        get_request.request_status=data['request_status']
        if data['request_status'].strip()=="Rejected":
            get_request.status=False
            get_request.save()
        else:
            get_request.save()
        return Response({"connect_staus":get_request.request_status})
    
    def delete(self,request):
        connectid=request.GET['connectid']
        fr=FriendRequests.objects.filter(id=connectid)
        if fr:
            fr.delete()
            return Response({"message":"deleted"})
        else:
            return Response({"message":"no found"})
           
    
"""Connected Profiles"""  
class ConnectedProfiles(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        
        query=Q(
            Q(request_status="Connected",requested_matrimony_id=matrimonyid)
            |
            Q(request_status="Connected",profile__matrimony_id=matrimonyid)
        )
        send_friend_request=FriendRequests.objects.select_related('profile').filter(query).order_by("-created_date")
        
        if send_friend_request.exists()==False:
            return Response([],status=200)
        response={}
        for view in send_friend_request:
            
            if matrimonyid==view.profile.matrimony_id:
               
               
                instance=get_object_or_404(Person,matrimony_id=view.requested_matrimony_id)
            else:
                
               
                instance=get_object_or_404(Person,id=view.profile.id)
                     
            serializer=GenderSerializer(instance,many=False).data
            serializer['connect_status']=view.request_status
            serializer['connectid']=view.id
            serializer['created_date']=view.created_date.strftime("%Y-%b-%d")
            serializer['updated_date']=view.updated_date.strftime("%Y-%b-%d")
           
            response[view.id]=serializer
        return Response(response.values())


"""RECEIVED(someone send me friend request) FRIEND REQUEST DATA"""  
class ReceivedFriendRequest(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        try:
            profile=Person.objects.get(matrimony_id=matrimonyid)
        except Exception as e:
            return Response({"message":"Invalid matrimony id","status":False,'error':str(e)},status=400)
               
        query=Q(
            Q(request_status="Waiting",
              requested_matrimony_id=profile.matrimony_id,
              status=True
              )
        )
        response={}
        received_requests=FriendRequests.objects.select_related('profile').filter(query).order_by("-updated_date")
        received_update=received_request(profile)
        all_request=chain(received_requests,received_update)
       
        for sender in all_request:
            try:
                instance=Person.objects.get(id=sender.self_profile.id)
                serializer=GenderSerializer(instance,many=False).data
                # serializer['connect_status']=""
                # serializer['connectid']=sender.id
                serializer['table']=2
                serializer['request_id']=sender.id
                serializer['notify']=sender.update_field_name
            except Exception:
                instance=Person.objects.get(id=sender.profile.id)
                serializer=GenderSerializer(instance,many=False).data
                serializer['connect_status']=""
                serializer['connectid']=sender.id
                serializer['table']=1
            
            serializer['created_date']=sender.created_date.strftime("%Y-%b-%d")
            serializer['updated_date']=sender.updated_date.strftime("%Y-%b-%d")
            
            response[random.randint(1000,9999)]=serializer
        return Response(response.values())
    
"""REJECTED FRIEND REQUEST"""
class RejectedFriendRequest(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        response={}
        try:
            profile=Person.objects.get(matrimony_id=matrimonyid)
        except Exception as e:
            return Response({"message":"Invalid mamtrimony id","error":str(e)},status=400)
               
        query=Q(
            Q(request_status="Rejected",requested_matrimony_id=profile.matrimony_id,status=False)
        )
        send_friend_request=FriendRequests.objects.select_related('profile')\
        .filter(query).order_by("-created_date")
        
        
        
        #decline update profile request
        get_decline=decline_requests(profile)
        all_request=chain(get_decline,send_friend_request)
        for sender in all_request:
            try:
                instance=Person.objects.get(id=sender.self_profile.id)
                serializer=GenderSerializer(instance,many=False).data
                serializer['table']=2
                serializer['request_id']=sender.id
                serializer['status']=sender.request_status
                serializer['notify']=sender.update_field_name
            except Exception:
                instance=Person.objects.get(id=sender.profile.id)
                serializer=GenderSerializer(instance,many=False).data
                serializer['connect_status']=sender.request_status
                serializer['connectid']=sender.id
                serializer['table']=1
            
            serializer['created_date']=sender.created_date.strftime("%Y-%b-%d")
            serializer['updated_date']=sender.updated_date.strftime("%Y-%b-%d")
            
            response[random.randint(1000,9999)]=serializer
        return Response(response.values())
        
        
        
        
        
        
        


"""number of  friend requests sended by me"""  
class GETSendedFriendRequest(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        try:
            profile=Person.objects.get(matrimony_id=matrimonyid)
        except Exception as e:
            return Response({"message":"Invalid mamtrimony id","error":str(e)},status=400)
        
        
        send_friend_request=profile.friendrequests_set.filter(request_status="Waiting")
        if send_friend_request:

            response={}
            for view in send_friend_request:
                profileid=Person.objects.get(matrimony_id=view.requested_matrimony_id)
                
                serializer=GenderSerializer(profileid,many=False).data
                serializer['connect_status']=view.request_status
                serializer['connectid']=view.id
                serializer['created_date']=view.created_date.strftime("%Y-%b-%d")
                serializer['updated_date']=view.updated_date.strftime("%Y-%b-%d")
            
                response[view.id]=serializer
            return Response(response.values())
        else:
            return Response([],status=200)


######################FINISH####################################


@api_view(['GET'])
def view_phone_nunmber(request):
    # if not request.POST._mutable:
    #     request.POST._mutable=True
    try:
        selfmid=request.GET['matrimony_id']
        othermid=request.GET['request_matrimony_id']
    except KeyError as e:
        return Response({"message":"mandatory keys","errors":str(e)},status=400)
    try:
        logged_profile=Person.objects.get(matrimony_id=selfmid)
    except Exception as e:
        return Response({"message":"Invalid matrimony id","errors":str(e)},status=400)
    try:
        request_profile=Person.objects.get(matrimony_id=othermid)
    except Exception as e:
        return Response({"message":"Invalid matrimony id","errors":str(e)},status=400)
    if logged_profile.gender==request_profile.gender:
        return Response({"message":"both are same gender"},status=200)
       
    phone_status=ViewedPhoneNumberStatus(logged_profile,request_profile)
    if phone_status:
        return Response({"message":"Allready add this profile in your Id",
                            "total_access":logged_profile.total_access,
                            "status":False},status=200)
    else:
        try:
            add_phone_number=ViewedPhonNumber.objects.get(profile=logged_profile)
        except Exception as e:
            add_phone_number=ViewedPhonNumber.objects.create(profile=logged_profile)
        add_phone_number.view.add(request_profile)
        logged_profile.total_access=str(int(logged_profile.total_access)-1)
        logged_profile.save()
        return Response({"message":"total access updated",
                            "total_access":logged_profile.total_access,
                            "status":False},status=200)
            



"""Partner Preference"""
class PartnerPreference(APIView):
    def get(self,request):
        pp=Partner_Preferences.objects.select_related('profile').filter(profile__matrimony_id=request.GET['matrimony_id'])
        if pp.exists():
            serializers=PPSerializers(pp[0],many=False)
            return Response(serializers.data)       
        else:
            return Response({"message":"No any Preferace Yet!"})    
    
    
            
    def put(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
        data=request.data
        pp=Partner_Preferences.objects.select_related('profile').get(profile__matrimony_id=request.GET['matrimony_id'])
              
        data['profile']=pp.profile.id
           
        serializers=PPSerializers(pp,data=data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Partner Preferance Updated successfully","status":True},status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors) 
            
    def delete(self,request):
        pp=Partner_Preferences.objects.select_related('profile').filter(profile__matrimony_id=request.GET['matrimony_id'])
        if pp.exists():
            pp.delete()
            return Response({"message":"Partner Preferance deleted successfully"})
        else:
            return Response({"message":"No record Yet"})


"""LIST OF PREMIUM USER"""
class PremiumUser(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        person=Person.objects.get(matrimony_id__iexact=matrimonyid)
        USER_PLAN=["Silver","Gold",'Diamond',"Platinum",'Trial']
        query=Q(
           ~ Q(gender=person.gender)
            &
            Q(block=False)
             &
            Q(active_plan__in=USER_PLAN)
            )
        response={}
        persons=Person.objects.filter(query).order_by('-reg_date')#[0:12]
        # :
        #     images=
        response=[{
                "image":person.profilemultiimage_set.latest('id').files.url if person.profilemultiimage_set.all() else None,
                "matimony_id":person.matrimony_id,
                "name":person.name,
                "dateofbirth":person.dateofbirth,
                "height":person.height,
                "active_plan":person.active_plan
                }for person in persons]
            # response[person.id].update(height_and_age(person.height,person.dateofbirth))
        return Response(response)
#only for testing  this post methods
    def post(self,request):
       
        USER_PLAN=["Silver","Gold",'Diamond',"Platinum"]
        query=Q(
            Q(active_plan__in=USER_PLAN)
            )
        response={}
        persons=Person.objects.filter(query).order_by('-reg_date')[0:12]
        for person in persons:
            images=ProfileMultiImage.objects.filter(profile__id=person.id)
            response[person.id]={
                "image":images[0].files.url if images.exists() else None,
                "matimony_id":person.matrimony_id,
                "name":person.name,
                "active_plan":person.active_plan,
                 "dateofbirth":person.dateofbirth,
                "height":person.height,
                }
            # response[person.id].update(height_and_age(person.height,person.dateofbirth))
        return Response(response.values())
        
            
""""FOR WEB APPICATION"""
class ProfileInfo(APIView):
    def get(self,request):
        matrimonyid=request.GET['matrimony_id']
        person=Person.objects.get(matrimony_id=matrimonyid)
        image=person.profilemultiimage_set.all()
        viewed_by_me=ViewedProfile.objects.filter(profile=person)
        FriendRequests.objects.filter(requested_matrimony_id=matrimonyid)
        response={
            "profileimage":image[0].files.url if image.exists() else None,
            "occupation":person.occupation,
            "name":person.name,
            "active_plan":person.active_plan,
            "viewed_by_me": viewed_by_me[0].view.count() if viewed_by_me.exists() else 0,
            "viewed_by_others":ViewedProfile.objects.filter(view__id=person.id).count(),
            "interest":FriendRequests.objects.filter(requested_matrimony_id=matrimonyid).count()
            }
        return Response(response)




"""HOME TAB"""

class HomeTabs(APIView):
    def get(self,request):
        import datetime
        matrimonyid=request.GET['matrimony_id']
        _q=request.GET['q'].strip()
        _list=['matches','new','premium','mutual','saw','viewed',
               'location','horoscope','qualification','star','occupation',
               'workplace'    
                             ]
        response={}
        if _q not in _list:
            return Response({"message":"This is not Valid query","status":False},status=403)
        try:
            person=Person.objects.get(matrimony_id=matrimonyid)
        except Exception as e:
            return Response({"message":"Invalid matrimony id","status":False},status=400)
        
        query=~Q(gender=person.gender)
        if _q=="matches":
            query
        elif _q=="new":
            india=pytz.timezone('Asia/Kolkata')
            interval_time=datetime.datetime.today().now(india) - datetime.timedelta(days=10)
            query=query & Q(reg_date__gte=interval_time)
        elif _q=="premium":
            USER_PLAN=["Silver","Gold",'Diamond',"Platinum","Trial"]
            query=query & Q(active_plan__in=USER_PLAN)
        elif _q=="mutual":
            query=Q(id__in=mutual_match(matrimonyid))
        
        elif _q=="saw":
            view_profile=ViewedProfile.objects.filter(profile=person)
            if view_profile.exists():
                query=Q(id__in= view_profile[0].view.all().values_list('id',flat=True))
            else:
                return Response([],status=200)
        elif _q=="viewed":
            
            view_profile=ViewedProfile.objects.filter(view__id=person.id)
            #query=Q(id__in=[i.profile.id for i in view_profile])
            query=Q(id__in=view_profile.values_list('profile__id',flat=True))
       
        elif _q=="location":
            query=query & Q(
                Q(city__iexact=person.city)
                |
                Q(state__iexact=person.state)
                |
                Q(mother_tongue__iexact=person.mother_tongue)
                
                )
            
        
        elif _q=="star":     
            query=query & Q(star=getattr(person,_q)) 
        elif _q=="occupation":
            query=query & Q(occupation=getattr(person,_q))     
        elif _q=="workplace":
            query=query & Q(workplace=getattr(person,_q))
        elif _q=="city":
            query=query & Q(city=getattr(person,_q))
        elif _q=="horoscope":
            query=query & Q(horoscope=getattr(person,_q))
        elif _q=="qualification":
            query=query & Q(
                ~Q(specialization=person.specialization)
                |
                ~Q(qualification=person.qualification)
                )
       
        persons=Person.objects.filter(query).order_by('-id')
        serializer=TabPersonSerializer(persons, context={'matrimony_id':matrimonyid},many=True)                         
        return Response(serializer.data)
        
        
        

    
"""TOTAL VIEW AND TOTAL REQUEST RECEIVE"""

@api_view(['GET'])
def get_total_number_request_and_view(request):
    matrimonyid=request.GET['matrimony_id']
    try:
        person=Person.objects.get(matrimony_id=matrimonyid)
    except Exception as e:
        return Response({"message":"error",
                         "status":False,"homeResponse":{"message":"Invalid matrimony id"}},status=400)
    try:
        #my profile viewed by other ,how many member viewed my profile
        viewed=ViewedProfile.objects.filter(view=person).count()
        
    except Exception as e:
         viewed=0
    total_request_receive=FriendRequests.objects \
    .filter(requested_matrimony_id=person.matrimony_id).only("requested_matrimony_id").count()
    homeImage=HomeScreenImage.objects.filter(status=True)
    #search_list=["viewed profile","response received","album","match maker","wedding planner","astrologer"]
    response={}
    for image in homeImage:
        if image.name=="viewed profile":
            response[image.id]={
                "id":image.id,
                "name":image.name,
                "image":image.image.url,
                "count":viewed
            }
        elif image.name=="response received":
            response[image.id]={
                 "id":image.id,
                 "name":image.name,
                "image":image.image.url,
                "count":total_request_receive
            }
        else:
            response[image.id]={
                    "id":image.id,
                    "name":image.name,
                    "image":image.image.url,
                    "count":0
                }
        
            
    # res ={
    #     "message":"success",
    #     "status":True ,
    #     "homeResponse":response.values()
    # }  
    return Response(response.values(),status=200)      
    
    
    
@api_view(['GET'])
def name(request):
    return Response({
    "message": "hello user"
})