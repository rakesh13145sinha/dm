
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *
# Create your views here.
class SubscriptionPla(APIView):
    def get(self,request):
        month=request.GET['month']
        plan=request.GET.get('membership')
        if plan is None:
            members=MemberShip.objects.filter(month=month).order_by('-id')
            serializers=SubscriptionSerializer(members,many=True)
            return Response(serializers.data) 
        elif plan is not None and month is not None: 
            members=MemberShip.objects.filter(month=month,subscription=plan).order_by('-id')
            serializers=SubscriptionSerializer(members,many=True)
            return Response(serializers.data)
        else:
            return Response({"message":"somthing wrong","status":False})
    def post(self,request):
        data=request.data 
        serializers=PlanSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Plan Posted successfully","status":True})
        else:
            print(serializers.errors)
            return Response(serializers.errors,status=400)
        
    def put(self,request):
        data=request.data
        planid=request.GET['planid']
        member=MemberShip.objects.get(id=planid)
        serializers=PlanSerializer(member,data=data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Plan Update successfully","status":True})
        else:
            print(serializers.errors)
            return Response(serializers.errors,status=400) 
        
    def delete(self,request):
        planid=request.GET['planid']
        member=MemberShip.objects.filter(id=planid)
        if member.exists():
            member.delete()
            return Response({"message":"Plan Deleted successfully","status":True})
        else:
            return Response({"message":"Invalid Id","status":True})