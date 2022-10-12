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
    path('profile/all',AllProfiles.as_view()),
    path('profile/',SingleProfile.as_view()),
    path('profile/connect/',SendFriendRequest.as_view()),
    path('profile/connect/send',SendFriendRequest.as_view()),
    path('profile/connect/received',ReceivedFriendRequest.as_view()),
    path('profile/connect/status',StautsOfSendRequest.as_view()),
    path('new/join',NewMatchProfile.as_view()),
    path('bookmark/',BookMarkProfile.as_view()),
   
    path('match/percentage',ProfileMatchPercentage.as_view()),
    path('match/daily',DailyRecomandation.as_view()),
    path('explor/',Explore.as_view()),
    path('explor/name',ExploreProfile.as_view()),
    
    #profile viewed and saw
    path('profile/saw',ISawProfile.as_view()),
    path('profile/viewed',WhoSawMyProfile.as_view()),
    #admin
    path('banner',Banner.as_view()),
   
    
]
