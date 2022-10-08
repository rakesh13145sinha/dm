from django.urls import path,include 
from .views import *
urlpatterns = [
    path('signup',Registration.as_view(),name="registration"),
    path('email/',Check_Email.as_view()),
    path('phone/',Check_Phone_Number.as_view()),
    path('state/',Nation.as_view()),
    path('verify/otp/',Validate_OTP.as_view())
]
