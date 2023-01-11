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
    query=Q(other_profile=otherid,update_field_name=data['update_field_name'],request_status="Waiting")
    try:
        selfid.updaterequests_set.get(query)
        return Response({"message":"Request allready done",},status=200)
    except Exception as e:
        
        selfid.updaterequests_set.create(other_profile=otherid,update_field_name=data['update_field_name'])
        return Response({"message":"Request sended successfully"},status=200)
    



