from django.urls import path
from .views import * 

urlpatterns = [
    path('person',search_by_matrimonyid)
]
