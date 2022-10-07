from django.urls import path,include 
from .views import *
urlpatterns = [
    path('signup',Registration.as_view(),name="registration"),
    path('email',Check_Email.as_view()),
    path('phone',Check_Phone_Number.as_view())
]
