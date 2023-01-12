from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.decorators import api_view
from account.models import Person 
from django.db.models import Q
from .models import *


"""Send request for update profile"""

@api_view(['POST'])
def generate_request(request):
    data=request.data
    try:
        #self matrimony id
        self_mid=request.GET['matrimony_id']
        #pass matrimony id which person what to send request,other person matrimony id
        other_mid=request.GET['requested_matrimony_id']
    except KeyError as e:
        return Response({"message":"Every key mandatory","error":str(e)},status=400)
    
    try:
        selfid=Person.objects.get(matrimony_id=self_mid)
    except Exception as e:
        return Response({"message":"Invalid matrimony id","error":str(e)},status=400)
    
    try:
        otherid=Person.objects.get(matrimony_id=other_mid)
    except Exception as e:
        return Response({"message":"Invalid matrimony id","error":str(e)},status=400)
    
    if selfid.gender==otherid.gender:
        return Response({"message":"You con't request this matrimony id"})
    
    dict_value=Person.objects.filter(matrimony_id=other_mid)\
    .values('drinking_habbit','rashi','star','dosham','smoking_habbit','diet_preference')
    updated_field=[key for key,value in dict_value[0].items() if value is None] 
    if data['update_field_name'] not in  updated_field  :
        return Response({"message":"This field allready updated"},status=200)                                    
    
    query=Q(other_profile=otherid,
            update_field_name=data['update_field_name'],
            request_status="Waiting",self_profile=selfid
            )
    try:
       
        UpdateRequests.objects.get(query)
        return Response({"message":"Request sent",},status=200)
    except Exception as e:
        
        UpdateRequests.objects.create(other_profile=otherid,\
                                      update_field_name=data['update_field_name'],\
                                       self_profile=selfid   
                                      )
        return Response({"message":"Request sent successfully"},status=200)
    
    


"""request reject"""
@api_view(['POST'])
def update_request(request):
    data=request.data
    try:
        #self matrimony id
        self_mid=request.GET['matrimony_id']
        tableid=request.GET['request_id']
    except KeyError as e:
        return Response({"message":"All Keys mandatory","error":str(e)},status=400)
    
    try:
        selfid=Person.objects.get(matrimony_id=self_mid)
    except Exception as e:
        return Response({"message":"Invalid matrimony id","error":str(e)},status=400)

    try:
        update_request=UpdateRequests.objects.get(id=tableid,other_profile=selfid)
    except Exception as e:
        return Response({"message":"Invalid request id"},status=400)
    
    update_request.request_status=data['request_status']
    update_request.save()
    return Response({"message":"Response updated successfully"},status=200)

