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
				('Waiting','Waiting')
				]
	user = models.OneToOneField(User,on_delete=models.CASCADE)

#basic info
	name = models.CharField(max_length=20,null=True)
	email=models.EmailField(null=True)
	matrimony_id = models.CharField(max_length=20,null=True)
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
	about_myself =  models.TextField()
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

class ProfileImage(models.Model):
	profile=models.OneToOneField(Person,on_delete=models.CASCADE)
	image=models.ImageField(upload_to="profile/image")

	

class ProfileMultiImage(models.Model):
	
	profile = models.ForeignKey(Person, on_delete=models.CASCADE)
	files = models.ImageField(upload_to = 'profile_pic/',null=True)
	
	def __str__(self):
		return "%s"%(self.id)

class SaveOTP(models.Model):
	
	phone_number = models.ForeignKey(Person, on_delete=models.CASCADE)
	otp = models.IntegerField(null=True) 
	
	
	
	def __str__(self):
		return "%s"%(self.phone_number)

# class Viewed_matches(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	viewed_user_id = models.CharField(max_length=100,null=True)
# 	#viewed_user_id = models.IntegerField(null=True)
# 	viewd_status = models.BooleanField(default=True)
	
# 	def __str__(self):
# 		return "%s"%(self.user.id)

# class LikedStatus(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	user_liked = models.CharField(max_length=100,null=True)
# 	LikedStatus = models.BooleanField(default=True)
	
# 	def __str__(self):
# 		return "%s" %(self.user.id)

# class Partner_Preferences(models.Model):
# 	profile = models.ForeignKey(Person, on_delete=models.CASCADE)
# # basic details
# 	min_age = models.CharField(max_length=100,null=True)
# 	max_age = models.CharField(max_length=100,null=True)
# 	min_height = models.CharField(max_length=100,null=True)
# 	max_height = models.CharField(max_length=100,null=True)
# 	physical_status = models.CharField(max_length=100,null=True)
# 	mother_tongue = models.CharField(max_length=100,null=True)
# 	marital_status = models.CharField(max_length=100,null=True)#multi
# 	drinking_habbit = models.CharField(max_length=100,null=True)
# 	smoking_habbit = models.CharField(max_length=100,null=True)
# 	food=models.CharField(max_length=200,null=True)
# # birth & religious	
# 	caste = models.CharField(max_length=100,null=True)
# 	religion = models.CharField(max_length=100,null=True)
# 	star = models.CharField(max_length=100,null=True)
# # education & profession
# 	occupation = models.CharField(max_length=100,null=True)#profession
# 	annual_income = models.CharField(max_length=100,null=True)
# 	job_sector = models.CharField(max_length=100,null=True)
# 	qualification	= models.CharField(max_length=100,null=True)
# # residential 
# 	city = models.CharField(max_length=100,null=True)
# 	state = models.CharField(max_length=100,null=True)
# 	country = models.CharField(max_length=100,null=True)
# 	dosham= models.CharField(max_length=100,null=True)
# 	profilecreate= models.CharField(max_length=100,null=True)
# 	assets= models.CharField(max_length=100,null=True)
	
# 	def __str__(self):
# 		return "%s" %(self.profile.user.id)

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

# class Height(models.Model):

# 	height=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('height',)	
# 	def __str__(self):
# 		return self.height

# class Religion(models.Model):

# 	religion=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('religion',)	
# 	def __str__(self):
# 		return self.religion

# class Qualification(models.Model):
	
# 	qualification=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('qualification',)	
# 	def __str__(self):
# 		return self.qualification

# class Under_graduation(models.Model):

# 	under_graduation=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('under_graduation',)	
# 	def __str__(self):
# 		return self.under_graduation

# class Post_graduation(models.Model):

# 	post_graduation=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('post_graduation',)	
# 	def __str__(self):
# 		return self.post_graduation

# class Super_speciality(models.Model):

# 	super_speciality=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('super_speciality',)	
# 	def __str__(self):
# 		return self.super_speciality

# class Rasi(models.Model):

# 	rasi=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('rasi',)	
# 	def __str__(self):
# 		return self.rasi

# class Age(models.Model):

# 	age=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('age',)	
# 	def __str__(self):
# 		return self.age

# class Stars(models.Model):
	
# 	stars=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('stars',)	
# 	def __str__(self):
# 		return self.stars

# class Mother_Occ(models.Model):

# 	mother_Occ=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('mother_Occ',)	
# 	def __str__(self):
# 		return self.mother_Occ

# class Father_Occ(models.Model):

# 	father_Occ=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('father_Occ',)	
# 	def __str__(self):
# 		return self.father_Occ

# class Food_Hobbit(models.Model):

# 	food_Hobbit=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('food_Hobbit',)	
# 	def __str__(self):
# 		return self.food_Hobbit

# class Drink_Hobbit(models.Model):

# 	drink_Hobbit=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('drink_Hobbit',)	
# 	def __str__(self):
# 		return self.drink_Hobbit

# class Smoke_Hobbit(models.Model):

# 	smoke_Hobbit=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('smoke_Hobbit',)	
# 	def __str__(self):
# 		return self.smoke_Hobbit

# class Job_sector(models.Model):

# 	job_sector=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('job_sector',)	
# 	def __str__(self):
# 		return self.job_sector

# class Gender(models.Model):

# 	gender=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('gender',)	
# 	def __str__(self):
# 		return self.gender

# class Caste(models.Model):

# 	caste=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('caste',)	
# 	def __str__(self):
# 		return self.caste

# class Annual_income(models.Model):

# 	annual_income=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('annual_income',)	
# 	def __str__(self):
# 		return self.annual_income

# class Marital_status(models.Model):

# 	marital_status=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('marital_status',)	
# 	def __str__(self):
# 		return self.marital_status

# class Physical_status(models.Model):

# 	physical_status=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('physical_status',)	
# 	def __str__(self):
# 		return self.physical_status

# class Mother_Tongue(models.Model):
	
# 	mother_Tongue=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('mother_Tongue',)	
# 	def __str__(self):
# 		return self.mother_Tongue

# class Created_by(models.Model):

# 	created_by=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('created_by',)	
# 	def __str__(self):
# 		return self.created_by

# class Citizen(models.Model):

# 	citizen=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('citizen',)	
# 	def __str__(self):
# 		return self.citizen

# class Profession(models.Model):

# 	profession=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('profession',)	
# 	def __str__(self):
# 		return self.profession

# class Birth_place(models.Model):

# 	birth_place=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('birth_place',)	
# 	def __str__(self):
# 		return self.birth_place

# class Family_type(models.Model):

# 	family_type=models.CharField(max_length=20)
# 	class Meta:
# 		unique_together = ('family_type',)	
# 	def __str__(self):
# 		return self.family_type

# class College(models.Model):

# 	college=models.CharField(max_length=100)
# 	class Meta:
# 		unique_together = ('college',)	
# 	def __str__(self):
# 		return self.college

# class Weight(models.Model):

# 	weight=models.CharField(max_length=100)
# 	class Meta:
# 		unique_together = ('weight',)	
# 	def __str__(self):
# 		return self.weight

# class FriendRequests(models.Model):

# 	request_status_types = (
# 		("Pending","Pending"),
# 		("Approved","Approved"),
# 		("Rejected","Rejected"),
# 		)

# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	requested_user_id = models.CharField(max_length=100,null=True)
# 	created_at = models.DateField()
# 	created_time = models.TimeField()
# 	request_status = models.CharField(choices = request_status_types, default="Pending", max_length = 25)
# 	updated_at = models.DateField()
# 	updated_time = models.TimeField()
# 	status = models.BooleanField(default=True)

# 	def __str__(self):
# 		return "%s"%(self.user)

# class MatchOfTheDay(models.Model):

# 	user_id = models.CharField(max_length=100,null=True)
# 	created_at = models.DateField()
# 	Ative_status = models.BooleanField(default=True)

# 	def __str__(self):
# 		return "%s"%(self.user_id)

# class VisibleDataRequest(models.Model):
# 	visible_status_types = (
# 		("Pending","Pending"),
# 		("Visible","Visible"),
# 		("Unvisible","Unvisible"),
# 		)
# 	main_user_id = models.CharField(max_length=100,null=True)
# 	visible_user_id = models.CharField(max_length=100,null=True)
# 	key_name = models.CharField(max_length=100,null=True)
# 	visible_status = models.CharField(choices = visible_status_types, default="Pending", max_length = 25)

# 	def __str__(self):
# 		return "%s"%(self.main_user_id)





# class SenderRequests(models.Model):
# 	request_status_types = (
# 		("Send","Send"),
# 		("Approved","Approved"),
# 		("Rejected","Rejected"),
# 		)
	
# 	sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True)#logged in userid
# 	request_for_user_id = models.CharField(max_length=100,null=True)#which profile you want to connect with pass the  user id here
# 	request_status = models.CharField(choices = request_status_types, default="Send", max_length = 25)
# 	created_at = models.DateField(auto_now=True,auto_now_add=False)
# 	created_time = models.TimeField(auto_now=True,auto_now_add=False)
# 	updated_at = models.DateField(auto_now=False,auto_now_add=True)
# 	updated_time = models.TimeField(auto_now=False,auto_now_add=True)
# 	status = models.BooleanField(default=False)

# 	def __str__(self):
# 		return "%s"%(self.sender)

# class ReceiveRequests(models.Model):
# 	received_status = (
# 		("Received","Received"),
# 		("Approved","Approved"),
# 		("Rejected","Rejected"),
# 		)
# 	profile = models.ForeignKey(User, on_delete=models.CASCADE,null=True)#logged in userid
# 	received_request = models.CharField(max_length=100,null=True)
# 	received_status = models.CharField(choices = received_status, default="Received", max_length = 25)
# 	created_at = models.DateField(auto_now=True,auto_now_add=False)
# 	created_time = models.TimeField(auto_now=True,auto_now_add=False)
# 	updated_at = models.DateField(auto_now=False,auto_now_add=True)
# 	updated_time = models.TimeField(auto_now=False,auto_now_add=True)
# 	status = models.BooleanField(default=False)
	
# 	def __str__(self):
# 		return "%s"%(self.profile)

# class MatchCountImage(models.Model):
# 	name= models.CharField(max_length=100)
# 	image=models.ImageField(upload_to='match_count/')
# 	def __str__(self):
# 		return (self.name)

# class Branch(models.Model):#mbbs,
# 	degree= models.CharField(max_length=100)
# 	image=models.ImageField(upload_to='match_count/')
# 	def __str__(self):
# 		return (self.degree)