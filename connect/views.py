import ast
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.decorators import api_view
from account.models import Person 
from django.db.models import Q
from .models import *
import random



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



"""document upload"""


class DocumentVerify(APIView):
    def get(self,request):
        id="The following documents to verify you profile details this will not be stored or shown to others members.Adhar card,PAN card,Driving License and Voter ID."
        slary_slip="Upload your salary slip(pay slip)and help us to verify your current salary it will not stored or shown members."
        docs_statement={
            "Id":id,
            "Photo":"Add photo to your profile and verify it .",
            "Salary_Slip":slary_slip,
            "Mobile":"Your mobile number verified successfully."
        }
        
        try:
            #self matrimony id
            self_mid=request.GET['matrimony_id']
        except KeyError as e:
            return Response({"message":"All Keys mandatory","error":str(e)},status=400)
        
        try:
            selfid=Person.objects.get(matrimony_id=self_mid)
        except Exception as e:
            return Response({"message":"Invalid matrimony id","error":str(e)},status=400)
        
       
        response={}
        for i in docs_statement.keys():
          
            try:
                doc=selfid.documentupload_set.get(name_of_documunt=i)
                status=doc.status
                upload=doc.upload_status
            except Exception as e:
                status=False
                upload=False
            response[random.randint(1000,9999)]={
                "name_of_document":i,
                "status":True if i=="Mobile" else status,
                "descriptions":docs_statement[i],
                "upload_status":upload

            }
        return Response(response.values())
    
    def post(self,request):
        if not request.POST._mutable:
            request.POST._mutable=True
            
        try:
            data = ast.literal_eval(request.data['registerdata'])
        except Exception as e:
        
            data=request.data
        try:
            #self matrimony id
            self_mid=request.GET['matrimony_id']
        except KeyError as e:
            return Response({"message":"All Keys mandatory","error":str(e)},status=400)
        
        try:
            selfid=Person.objects.get(matrimony_id=self_mid)
        except Exception as e:
            return Response({"message":"Invalid matrimony id","error":str(e)},status=400)
        
        doc_name_list=['Id',"Photo","Salary_Slip","Mobile"]
        if data['name'] not in doc_name_list:
            return Response({"message":"document name invalid"},status=400)
        get,create=DocumentUpload.objects.get_or_create(profile=selfid,document=request.FILES['document'],name_of_document=data['name'],upload_status=True)
        if create:
            return Response({"message":"Document uploaded successfully.Wait for update"},status=200)
        else:
            return Response({"message":"Document allready uploaded"},status=200)

