from django.urls import path,include 
from .views import *
urlpatterns = [
    path('signup',Registration.as_view(),name="registration"),
    path('signup/field/update',NeedToUpdateFields.as_view()),
    path('email/',Check_Email.as_view()),
    path('phone/',Check_Phone_Number.as_view()),
    path('state/',Nation.as_view()),
    path('verify/otp/',Validate_OTP.as_view()),
    
    #image upload
    path('image/upload/',UploadProfileImage.as_view()),
    path('new/match',OppositeGenderProfile.as_view()),
    path('new/join',NewMatchProfile.as_view()),
    path('bookmark/',BookMarkProfile.as_view()),
    path('profile/',SingleProfile.as_view()),
    path('match/percentage',ProfileMatchPercentage.as_view()),
    path('match/daily',DailyRecomandation.as_view()),
    path('explor/',Explore.as_view())
]
