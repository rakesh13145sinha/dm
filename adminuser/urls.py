from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard',dashboard),
    path('gender',gender)
]
