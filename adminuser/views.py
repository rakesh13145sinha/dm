from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from account.models import *
from django.db.models import Count,Q

# Create your views here.
@api_view(['GET'])
def dashboard(request):
    dashboard=Person.objects.\
    aggregate(male=Count("gender",filter=Q(gender="Male")),
             female=Count("gender",filter=Q(gender="Female")),
             subscribe=Count("active_plan",filter=Q(active_plan='Trial')))
    return Response(dashboard)


@api_view(['GET'])
def gender(request):
    profiles=Person.objects.filter(gender=request.GET['gender']).only('id')
    response={}
    for pro in profiles:
        images=pro.profilemultiimage_set.all()
        response[pro.id]={
            "id":pro.id,
            "matrimony_id":pro.matrimony_id,
            "image":[{"image":i.files.url} for i in images],
            "gender":pro.gender,
            "name":pro.name,
            "phone_number":pro.phone_number,
            "status":pro.status
            
        }
        
        
    return Response(response.values(),status=200)
    

        
    

    
    