from django.db import models

from django.contrib.auth.models import User



class Person(models.Model):
	GENDER=[('Male','Male'),('Female','Female')]
	MATRIMONY=[
				('Married','Married'),
				('UnMarried','UnMarried'),
				('Widow','Widow'),
				('widower','widower'),
				('Divorce','Divorce'),
				('Ready To Divorce','Ready To Divorce'),
				]
	USER_PLAN=[
				("Expire","Expire"),("Silver","Silver")
				,("Gold","Gold"),('Diamond','Diamond'),
				('Waiting','Waiting'),("Combo","Combo"),("Platinum","Platinum")
				]
	user = models.OneToOneField(User,on_delete=models.CASCADE)
#66014444
#basic info
	name = models.CharField(max_length=20,null=True)
	email=models.EmailField(null=True)
	matrimony_id = models.CharField(max_length=20,null=True,blank=True)
	phone_number = models.CharField(max_length=13,null=True)
	gender = models.CharField(max_length=20,null=True,choices=GENDER)
	dateofbirth = models.CharField(max_length=20,null=True)
	image=models.ImageField(upload_to="profile/image",null=True,blank=True)

#physical status
	height = models.CharField(max_length=100,null=True)
	physical_status = models.CharField(max_length=100,null=True)
	weight	= models.CharField(max_length=100,null=True)
	

#life status
	marital_status	= models.CharField( max_length=100,null=True,choices=MATRIMONY)
	mother_tongue = models.CharField(max_length=100,null=True)
	diet_preference	= models.CharField(max_length=100,null=True)
	drinking_habbit	= models.CharField(max_length=100,null=True)	
	smoking_habbit	= models.CharField(max_length=100,null=True)
	
#caster & religious
	
	gotram	= models.CharField(max_length=100,null=True)
	star	= models.CharField(max_length=100,null=True)
	rashi = models.CharField(max_length=100,null=True)
	caste = models.CharField(max_length=100,null=True)
	sub_caste	= models.CharField(max_length=100,null=True)
	religion = models.CharField(max_length=100,null=True)
	horoscope=models.CharField(max_length=200,null=True)
	habbits=models.CharField(max_length=200,null=True)
	workplace=models.CharField(max_length=20,null=True)
	
#location & contact
	city = models.CharField(max_length=100,null=True)
	state = models.CharField(max_length=100,null=True)
	country = models.CharField(max_length=100,null=True)

	

#profession & education
	occupation = models.CharField(max_length=100,null=True)
	annual_income = models.CharField(max_length=100,null=True)
	job_sector = models.CharField(max_length=100,null=True)
	college	= models.CharField(max_length=100,null=True)
	orgnisation=models.CharField(max_length=255,null=True)
	qualification	= models.CharField(max_length=100,null=True)
	

#family details
	total_family_members = models.CharField(max_length=100,null=True)
	father_details = models.CharField(max_length=100,null=True)
	mother_details = models.CharField(max_length=100,null=True)
	unmarried_brother=models.IntegerField(null=True)
	married_brother=models.IntegerField(null=True)
	unmarried_sister=models.IntegerField(null=True)
	married_sister=models.IntegerField(null=True)
	profile_created_by=models.CharField(max_length=200,null=True)
	

#family type
	family_type = models.CharField(max_length=100,null=True)
	family_status = models.CharField(max_length=100,null=True)
	family_value = models.CharField(max_length=100,null=True)

#about self	
	about_myself =  models.TextField(null=True,blank=True)
	status=models.BooleanField(default=True)
	block=models.BooleanField(default=False)
	verify=models.BooleanField(default=False)
	
#only admin perpose
	active_plan=models.CharField(max_length=100,null=True,choices=USER_PLAN,blank=True,default="Waiting")
	total_access=models.IntegerField(null=True,blank=True,default=0)
	
	reg_date=models.DateTimeField(auto_now=True,auto_now_add=False)
	reg_update=models.DateTimeField(auto_now=False,auto_now_add=True)
	

	class Meta:
		unique_together = ("phone_number","matrimony_id",'email')
	
	def __str__(self):
		return "%s" %(self.user)

	
class Bookmark(models.Model):
    profile=models.OneToOneField(Person,on_delete=models.CASCADE)
    album=models.ManyToManyField(Person,related_name="album")
    

	

class ProfileMultiImage(models.Model):
	profile = models.ForeignKey(Person, on_delete=models.CASCADE)
	files = models.ImageField(upload_to = 'profile_pic/',null=True)
	
	def __str__(self):
		return "%s"%(self.id)

class SaveOTP(models.Model):

	phone_number = models.CharField(max_length=50,null=True)
	otp = models.IntegerField(null=True) 
	
	
	
	def __str__(self):
		return "%s"%(self.phone_number)


class ViewedProfile(models.Model):
	profile=models.OneToOneField(Person,on_delete=models.CASCADE)
	view=models.ManyToManyField(Person,related_name="viewprofile")
	



class Partner_Preferences(models.Model):
	profile = models.OneToOneField(Person, on_delete=models.CASCADE)
# basic details
	min_age = models.CharField(max_length=100,null=True)
	max_age = models.CharField(max_length=100,null=True)
	min_height = models.CharField(max_length=100,null=True)
	max_height = models.CharField(max_length=100,null=True)
	physical_status = models.CharField(max_length=100,null=True)
	mother_tongue = models.CharField(max_length=100,null=True)
	marital_status = models.CharField(max_length=100,null=True)#multi
	drinking_habbit = models.CharField(max_length=100,null=True)
	smoking_habbit = models.CharField(max_length=100,null=True)
	food=models.CharField(max_length=200,null=True)
# birth & religious	
	caste = models.CharField(max_length=100,null=True)
	religion = models.CharField(max_length=100,null=True)
	star = models.CharField(max_length=100,null=True)
# education & profession
	occupation = models.CharField(max_length=100,null=True)#profession
	annual_income = models.CharField(max_length=100,null=True)
	job_sector = models.CharField(max_length=100,null=True)
	qualification	= models.CharField(max_length=100,null=True)
# residential 
	city = models.CharField(max_length=100,null=True)
	state = models.CharField(max_length=100,null=True)
	country = models.CharField(max_length=100,null=True)
	dosham= models.CharField(max_length=100,null=True)
	profilecreate= models.CharField(max_length=100,null=True)
	assets= models.CharField(max_length=100,null=True)
	
	def __str__(self):
		return "%s" %(self.profile.user.id)

class Country(models.Model):
	name= models.CharField(max_length=20)

	class Meta:
		unique_together = ("name",)
	def __str__(self):
		return self.country

class State(models.Model):

	name=models.CharField(max_length=20)
	country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		unique_together = ("name",)	
	def __str__(self):
		return self.state
		
class City(models.Model):

	name=models.CharField(max_length=20)
	state=models.ForeignKey(State, on_delete=models.CASCADE)

	class Meta:
		unique_together = ("name",)

	def __str__(self):
		return self.city

class BannerImage(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='banner')
    background=models.CharField(max_length=20,null=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.name



class FriendRequests(models.Model):

	request_status_types = (
		("Connect","Connect"),
		("Connected","Connected"),
		("Waiting","Waiting"),
		("Rejected","Rejected"),
		)

	profile = models.ForeignKey(Person, on_delete=models.CASCADE)
	requested_matrimony_id = models.CharField(max_length=100,null=True)
	request_status = models.CharField(choices = request_status_types, default="Waiting", max_length = 25)

	created_date=models.DateTimeField(auto_now=True,auto_now_add=False)
	updated_date=models.DateTimeField(auto_now=False,auto_now_add=True)
	status=models.BooleanField(default=False)
	











