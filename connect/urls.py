from django.urls import path 
from .views import * 
urlpatterns = [
    path('update',generate_request,name="send request for update profile")
   
]
