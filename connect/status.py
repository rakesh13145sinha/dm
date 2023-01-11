from account.models import Person 
from django.db import Q
from .models import UpdateRequests


def delete_request(selfmid,field_choices):
    for field in field_choices: 
        get_item=UpdateRequests.objects.filter(other_profile=selfmid,update_field_name=field)
        if get_item:
            get_item.delete()
        else:
            pass 
    return "removed generated request"
   
       
            

    