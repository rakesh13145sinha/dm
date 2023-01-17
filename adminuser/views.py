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
    annotate(male=Count("gender",filter=Q(gender="Male")),
             female=Count("gender",filter=Q(gender="Female")),
             subscribe=Count("active_plan",filter=Q(active_plan='Trial')))
    return Response({"data":dashboard.values("male","female","subscribe")})
    