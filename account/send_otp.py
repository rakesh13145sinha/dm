from sendotp import sendotp
import requests
import urllib
import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv('.env')
template_id=os.environ.get("template_id")
access_key =os.environ.get("access_key") 







def sending_otp(otp,phone):
	
	url = "https://api.msg91.com/api/v5/otp?template_id="+template_id +"&mobile=91"+phone+"&authkey="+access_key+"&otp="+str(otp)
	#urllink="https://api.msg91.com/api/v5/otp?template_id=60fa666d132e3b5463407c09&mobile=917004269606&authkey=364668A3kfs0Kel3Ld60fa4eaaP1&otp=1253"
	#Run API
	r = requests.get(url)
	
	return r.text