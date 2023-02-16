import requests
from decouple import config 
template_id=config("template_id")
access_key =config("access_key")
from .models import SaveOTP 


def sending_otp(otp,phone):
   
    SaveOTP.objects.update_or_create(phone_number=phone,otp=2023)
    

    url = "https://api.msg91.com/api/v5/otp?template_id="+template_id +"&mobile=91"+phone+"&authkey="+access_key+"&otp="+str(otp)
    #urllink="https://api.msg91.com/api/v5/otp?template_id=60fa666d132e3b5463407c09&mobile=917004269606&authkey=364668A3kfs0Kel3Ld60fa4eaaP1&otp=1253"
    #Run API
    r = requests.get(url)



    return r.text