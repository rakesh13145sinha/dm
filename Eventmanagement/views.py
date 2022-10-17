from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import * 
from .serializers import *
from .category import *
from account.models import Person

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
            return Response([{"name":i}  for i in Plannerdata[planner]],status=200) 
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
                serializers=EventSerializer(event[0],many=False).data
                
                serializers['album']=[{"id":i.id,"image":i.image.url}  for i in event[0].eventmultiimage_set.all() ]
                serializers['project']=[{"id":i.id,"name_of_project":i.name_of_project, "image":i.image.url}  for i in event[0].project_set.all() ]
                serializers['review']=[{"id":i.id,"review":i.review }  for i in event[0].review_set.all() ]
                return Response(serializers)
            else:
                return Response({"message":"Event Id Not Found",'status':False},status=400)
        
        elif vendorname is not None :
            try:
                vendor=Vendor.objects.get(vendor_name=vendorname,status=True)
            except Exception as msg:
                return Response({"message":"Vendor May be Incorrect","status":False},status=200)
            serializers=EventSerializer(vendor.ventorevent_set.filter(status=True),many=True)
            return Response(serializers.data)
        
        elif category is not None:
            event=VentorEvent.objects.filter(category=category,status=True)
            if event.exists():
                serializers=EventSerializer(event[0],many=True).data
                return Response(serializers)
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


"""EVENT LIKES"""
class LikesView(APIView):
    def post(self,request):
        matrimonyid=request.GET['matrimony_id']
        profile=Person.objects.get(matrimony_id=matrimonyid)
        event=VentorEvent.objects.get(id=request.GET['eventid']) 
        if event.likes.filter(matrimony_id=matrimonyid).exist():
            event.likes.remove(profile)
            return Response({"likes":False,"status":False},status=200)
        else:
            event.likes.add(profile)
            return Response({"likes":True,"status":True},status=200)
        
        
"""Multiple Image upload"""
class Album(APIView):
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
        
        event=VentorEvent.objects.get(id=request.GET['eventid'])
        files=request.FILES.getlist('image')
        for img in files:
            EventMultiImage.objects.create(event_planner=event,image=img)
        return Response({"message":"Image Uploaded successfully","status":True},status=200)
    
    
"""Multiple Project Upload"""
class Menu(APIView):
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
        data=request.data
        event=VentorEvent.objects.get(id=request.GET['eventid'])
        Project.objects.create(event_planner=event,image=data['image'],name_of_project=data['name_of_project'])
        return Response({"message":"Project successfully","status":True},status=200)
    


"""REVIEW """
class LeaveReview(APIView):
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
        data=request.data
        matrimonyid=request.GET['matrimony_id']
        profile=Person.objects.get(matrimony_id=matrimonyid)
        event=VentorEvent.objects.get(id=request.GET['eventid'])
        Review.objects.create(event_planner=event,profile=profile,review=data['review'])
        return Response({"message":"Thanks for review","status":True},status=200)