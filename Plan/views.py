import razorpay
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Person
from .models import *
from .serializers import *
from account.models import Person

from django.db.models import Q
from decouple import config
from rest_framework.decorators import api_view
from datetime import timedelta
import datetime 
import pytz 

# Create your views here.
"""get Plans"""
@api_view(['GET'])
def subscription_plan(request):
    plan=request.GET['q']
    if plan is not None:
        plans=MemberShip.objects.filter(days=int(plan))
        serializers=PlanSerializer(plans,many=True)
        return Response(serializers.data)
    else:
        return Response({"message":"Invalid request"},status=200)
     
   
        


"""PAYMENT POST"""
class PaymentCapture(APIView):
    
    def get(self,request):
        planid=request.GET['planid']
        matrimonyid=request.GET['matrimony_id']
        KEY=config("KEY")
        SECRET =config("SECRET")
        try:
            plan=MemberShip.objects.get(id=planid)
        except Exception as msg:
            print(msg)
            return Response({"message":"Plan Id Not Valid","status":False},status=400)
        
        try:
            profile=Person.objects.get(matrimony_id=matrimonyid)
        except Exception as msg:
            print(msg)
            return Response({"message":"Invalid Matrimony Id","status":False},status=400)
        client = razorpay.Client(auth=(KEY,SECRET))

        payment=client.order.create({"amount": int(plan.price)*100,"currency": "INR","payment_capture":1})
        
        data={"message":"oderid generated successfully",
              "status":True,"orderid":payment['id'],
              "email":profile.email,
              "name":profile.name,
              "phone_number":profile.phone_number
              
              }
        
        return Response(data,status=200)
           
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True 
        data=request.data
        matrimonyid=request.GET['matrimony_id']
        query=Q(
             Q (matrimony_id=matrimonyid)
            &
            Q(active_plan="Waiting")
        )
        profile=Person.objects.filter(query)
        if profile.exists==False:
            return Response({"message":"Your are premium user","status":False},status=200)
        
        planid=request.GET['planid']
        data['profile']=matrimonyid
        data['status']=True
        data["membership"]=planid
        serializers=PaymentSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Payment sucessfully updated","status":True},status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors,status=200)
        
        
    def delete(self,request):
        paymenetid=request.GET['paymentid']
        payment=Payment.objects.filter(id=paymenetid)
        if payment.exists():
            payment.delete()
            return Response({"message":"Payment Id deleted",'status':True})
        else:
            return Response({"message":"Invalid Payment Id","status":False})

"""Payment record"""       
class GetAllPayment(APIView):
    def get(self,request):
        matrimonyid=request.GET.get('matrimony_id')
        response={}
        if matrimonyid is not None:
            profile=Person.objects.get(matrimony_id=matrimonyid)
            subscriptions=Payment.objects.filter(profile=matrimonyid).order_by('-id')
            for pay in subscriptions:
                serializer=PaymentSerializer(pay,many=False).data 
                serializer['name']=profile.name
                serializer['matrimony_id']=profile.matrimony_id
                response[pay.id]=serializer
            return  Response(response.values())
        else:
            subscriptions=Payment.objects.all().order_by('-id')
            
            for pay in subscriptions:
                person=Person.objects.get(matrimony_id=pay.profile)
                serializer=PaymentSerializer(pay,many=False).data 
                serializer['name']=person.name
                serializer['matrimony_id']=person.matrimony_id
                response[pay.id]=serializer
                
            return  Response(response.values())
    
"""FREE TRIAL API""" 
@api_view(['GET'])
def take_free_trial(request):
    try:
        taken_planid=request.GET['plan_id']
        mid=request.GET['matrimony_id']
    except Exception as e:
        return Response({"message":"Key error","error":str(e)},status=400)
    try:
        profile=Person.objects.get(matrimony_id=mid)
    except Exception as e:
        return Response({"message":"Invalid matrimony_id"},status=400)
    try:
        plan=MemberShip.objects.get(id=taken_planid)
        if plan.subscription!="Trial":
            return Response({"message":"We are Test Beta vesion,User can chooice only trial plan"},status=200)
            
    except Exception as e:
        return Response({"message":"Invalid planid"},status=400)
    _taken_plan=["Expire","Waiting"]
				
				
				
    if profile.active_plan not in _taken_plan:
        return Response({"message":"You have already one plan"},status=200)
    
    
    india=pytz.timezone('Asia/Kolkata')
    expiry_date=timedelta(days=15)
    today_date=datetime.datetime.today().date(india)
    profile.active_plan=plan.subscription
    profile.total_access=plan.total_access
    profile.plan_taken_date=today_date
    profile.plan_expiry_date=today_date+expiry_date
    profile.save()
    return Response({"message":"Now you are in trial plan"},status=200)
    
