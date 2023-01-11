from account.models import Person 
from django.db import Q
from .models import UpdateRequests


def generate_request(selfmid,othermid,field_choice):
   
    try:
        
        selfmid.updaterequests_set\
        .get(other_profile=othermid,update_field_name=field_choice,request_status="Waiting")
        return "Waiting"
    except Exception :
        try:
            selfmid.updaterequests_set\
            .get(other_profile=othermid,update_field_name=field_choice,request_status="Accepted")
            return "Accepted"
        except Exception :
           
            exists=selfmid.updaterequests_set\
            .filter(other_profile=othermid,update_field_name=field_choice,request_status="Rejected")
            if exists:
                return "Request"
            else :
                return "Request"
       
            

    