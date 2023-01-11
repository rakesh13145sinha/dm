from account.models import Person 
from .models import UpdateRequests


def delete_request(selfmid,field_choices):
    for field in field_choices: 
        get_item=UpdateRequests.objects.filter(other_profile=selfmid,update_field_name=field)
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
   
       
            

    