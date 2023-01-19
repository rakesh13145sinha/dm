from django.urls import path,include 
from .views import *
urlpatterns = [
    path('signup',Registration.as_view(),name="registration"),
    path('preferance/',PartnerPreference.as_view()),
    path('signup/field/update',NeedToUpdateFields.as_view()),
    path('email/',Check_Email.as_view()),
    path('phone/',Check_Phone_Number.as_view()),
    path('state/',Nation.as_view()),
    path('verify/otp/',Validate_OTP.as_view()),
    
    #image upload
    path('image/upload/',UploadProfileImage.as_view()),
    
    
    path('new/match',OppositeGenderProfile.as_view()),##
   
    path("profile/",include([ 
                             
                             
        path('premium/',PremiumUser.as_view()),###
    
        path('info/',ProfileInfo.as_view()),
        path('',SingleProfile.as_view()),
        path('complete',ProfileUpdatePercentage.as_view()),
        path('connect/',SendFriendRequest.as_view()),
        path('connect/send',GETSendedFriendRequest.as_view()),
        path('connect/receive',ReceivedFriendRequest.as_view()),
        path('connect/reject',RejectedFriendRequest.as_view()),
        path('connect/accepted',ConnectedProfiles.as_view()),
        path("summary",get_total_number_request_and_view),
                          
                             ])),
    
    
    path('mobile/view',view_phone_nunmber),  
    path('bookmark/',BookMarkProfile.as_view()),
    path('bookmark/show',Album.as_view()),
    path('match/percentage',profile_match_percentage),
    
    path('match/daily',DailyRecomandation.as_view()),
    path('explor/',Explore.as_view()),
    
    
    path('tab/',HomeTabs.as_view(),name="home tab"),
    path('banner',Banner.as_view()),
    path('test',name)
   
    
]
