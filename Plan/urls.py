from django.urls import path 
from .views import *
urlpatterns = [
    path('',subscription_plan),
    path("payment/",PaymentCapture.as_view()),
    path('payment/check',GetAllPayment.as_view()),
    path('trial',take_free_trial,name="trial vesion")
]
