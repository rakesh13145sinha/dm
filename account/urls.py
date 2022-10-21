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
    path('new/join',NewMatchProfile.as_view()),###
    path('profile/all',AllProfiles.as_view()),###
    path('profile/premium/',PremiumUser.as_view()),###
    path('match/mutual/',MatchInPercentage.as_view()),###
    path('profile/saw',ISawProfile.as_view()),###
    path('profile/viewed',WhoSawMyProfile.as_view()),###
    path('explor/name',ExploreProfile.as_view()),###
    
    
    path('profile/info/',ProfileInfo.as_view()),
    path('profile/',SingleProfile.as_view()),
    path('profile/complete',ProfileUpdatePercentage.as_view()),
    path('profile/connect/',SendFriendRequest.as_view()),
    path('profile/connect/send',GETSendedFriendRequest.as_view()),
    path('profile/connect/receive',ReceivedFriendRequest.as_view()),
    path('profile/connect/reject',RejectedFriendRequest.as_view()),
    path('profile/connect/accepted',ConnectedProfiles.as_view()),
    
    
    path('bookmark/',BookMarkProfile.as_view()),
    path('bookmark/show',Album.as_view()),
    path('match/percentage',ProfileMatchPercentage.as_view()),
    
    path('match/daily',DailyRecomandation.as_view()),
    path('explor/',Explore.as_view()),
    
    
    #profile viewed and saw
    
    
    #admin
    path('tab/',HomeTabs.as_view(),name="home tab"),
    path('banner',Banner.as_view()),
   
    
]
