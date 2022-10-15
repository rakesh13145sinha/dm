import razorpay
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Person
from .models import *
from .serializers import *
from account.models import Person
load_dotenv('.env')
import os


# Create your views here.
class SubscriptionPla(APIView):
    def get(self,request):
        month=request.GET.get('month')
        plan=request.GET.get('membership')
        planid=request.GET.get('planid')
       
        if plan is not  None:
            members=MemberShip.objects.filter(month=month).order_by('-id')
            serializers=SubscriptionSerializer(members,many=True)
            return Response(serializers.data) 
        elif plan is not None and month is not None:
            print("============xxxxxxxxxxxxxxx===============") 
            members=MemberShip.objects.filter(month=month,subscription=plan).order_by('-id')
            serializers=SubscriptionSerializer(members,many=True)
            return Response(serializers.data)
        elif planid is not None:
            print("============yyyyyyyyyyyyyyyyyyyyy===============")
            members=MemberShip.objects.get(id=planid)
            serializers=SubscriptionSerializer(members,many=False)
            return Response(serializers.data)
        else:
            members=MemberShip.objects.all().order_by('-id')
            serializers=SubscriptionSerializer(members,many=True)
            return Response(serializers.data)
        return Response({"message":"somthing wrong","status":False})
    
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
        data=request.data 
        data['status']=True
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
        


"""PAYMENT POST"""
class PaymentCapture(APIView):
    
    def get(self,request):
        planid=request.GET['planid']
        matrimonyid=request.GET['matrimony_id']
        KEY=os.environ.get("KEY")
        SECRET =os.environ.get("SECRET")
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
        matrimonyid=request.GET.get('   ')
        response={}
        if matrimonyid is not None:
            profile=Person.objects.get(matrimony_id=matrimonyid)
            subscriptions=Payment.objects.filter(profile=matrimonyid).order_by('-id')
            for pay in subscriptions:
                
                response[pay.id]={
                    "id":pay.id,
                    "name":profile.name,
                    "matrimony_id":profile.matrimony_id,
                    "planid":pay.membership,
                    "matrimonyid":pay.profile,
                    "taken data":pay.created_date
                }
            return  Response(response.values())
        else:
            subscriptions=Payment.objects.all().order_by('-id')
            
            for pay in subscriptions:
                person=Person.objects.get(matrimony_id=pay.profile)
                response[pay.id]={
                    "id":pay.id,
                    "name":person.name,
                    "matrimony_id":person.matrimony_id,
                    "planid":pay.membership,
                    "matrimonyid":pay.profile,
                    "taken data":pay.created_date
                }
            return  Response(response.values())
                  