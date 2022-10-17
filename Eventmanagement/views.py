from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import * 
from .serializers import *
from .category import *

class VenderoView(APIView):
    def get(self,request):
        
        serializers=VendorSerializer(Vendor.objects.filter(status=True),many=True)
        return Response(serializers.data)
    def post(self,request):
        data=request.data 
        serializers=VendorSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Vendor Create Successfully","status":True},status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors)
    def put(self,request):
        data=request.data 
        vendor=Vendor.objects.get(id=request.GET['vendorid'])
        serializers=VendorSerializer(vendor,data=data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Vendor Updated Successfully","status":True},status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors)
    def delete(self,request):
        message=request.GET.get('delete all')
        vendor=Vendor.objects.filter(id=request.GET['vendorid'])
        if vendor.exists():
            vendor.delete() 
            return Response({"message":"Vendor Deleted Successfully","status":True},status=200)
        elif message is not None:
            Vendor.objects.all().delete()
            return Response({"message":"Vendor All Deleted Successfully","status":True},status=200)
        else:
           
            return Response({"message":"Vendor Id Not Found","status":False},status=400)
        

class PlannerCategory(APIView):
    def get(self,request):
        planner=request.GET['planner']
        if Plannerdata.get(planner):
            return Response(Plannerdata[planner],status=200) 
        else:
            return Response({"message":"May Incorrect Planner Name"})      

class VendorEventView(APIView):
    def get(self,request):
        eventid=request.GET.get('eventid')
        vendorname=request.GET.get('vendor_name')
        category=request.GET.get('category_name')
        if eventid is not None:
            event=VentorEvent.objects.filter(id=eventid,status=True)
            if event.exists():
                serializers=EventSerializer(event[0],many=False)
                return Response(serializers.data)
            else:
                return Response({"message":"Event Id Not Found",'status':False},status=400)
        
        elif vendorname is not None :
            vendor=Vendor.objects.get(vendor_name=vendorname)
            serializers=EventSerializer(vendor.ventorevent_set.filter(status=True),many=True)
            return Response(serializers.data)
        elif category is None:
            event=VentorEvent.objects.filter(category=category,status=True)
            if event.exists():
                return EventSerializer(event[0],many=False).data
            else:
                return Response([],status=200)
            
        else:
            serializers=EventSerializer(VentorEvent.objects.filter(status=True),many=True)
            return Response(serializers.data)
    
    def post(self,request):
        data=request.data 
        
        vendor=Vendor.objects.get(vendor_name=request.GET['name'])
        data["vendor"]=vendor.id
        serializers=EventSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Vendor Event Created Successfully","status":True},status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors)
    def put(self,request):
        data=request.data 
        event=VentorEvent.objects.get(id=request.GET['eventid'])
        serializers=EventSerializer(event,data=data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":"Vendor Create Successfully","status":True},status=200)
        else:
            print(serializers.errors)
            return Response(serializers.errors)
    def delete(self,request):
        message=request.GET.get('delete all')
        event=VentorEvent.objects.filter(id=request.GET['eventid'])
        if event.exists():
            event.delete() 
            return Response({"message":"Vendor Event Deleted Successfully","status":True},status=200)
        elif message is not None:
            VentorEvent.objects.all().delete()
            return Response({"message":"Vendor Event All Deleted Successfully","status":True},status=200)
        else:
           
            return Response({"message":"Vendor Event Id Not Found","status":False},status=400)