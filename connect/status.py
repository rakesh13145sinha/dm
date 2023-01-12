from account.models import Person 
from .models import UpdateRequests


"""After update profile this request will delete if any requested to you update profile """
def delete_request(selfmid,field_choices):
    for field in field_choices: 
        get_item=UpdateRequests.objects.filter(other_profile=selfmid,update_field_name=field,request_status="Waiting")
        if get_item:
            get_item.delete()
        else:
            pass 
    return "removed generated request"

def request_status(selfmid,othermid,field_choices):
    response={
        "drinking_habbit":False,
        "rashi":False,
        "star":False,
        "smoking_habbit":False,                              
        "diet_preference":False,
        "dosham":False,
        
    }
    for field in field_choices:
        try:
            UpdateRequests.objects\
            .get(self_profile=selfmid,other_profile=othermid,update_field_name=field)
            response[field]=True  
        except Exception:
            pass
    
    return response 


"""received request for update"""
def received_request(midobject) :
    
    get_item=UpdateRequests.objects.filter(other_profile=midobject,request_status="Waiting")
   
    return get_item


"""Get all decline request """      
def decline_requests(midobject): 
    
    get_decline_request=UpdateRequests.objects.filter(other_profile=midobject,request_status="Rejected")
        
    return get_decline_request
     
       
            

    