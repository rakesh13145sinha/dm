from django.urls import path 
from .views import *
urlpatterns = [
    path('',SubscriptionPla.as_view()),
    path("payment/",PaymentCapture.as_view()),
    path('payment/check',GetAllPayment.as_view())
]
