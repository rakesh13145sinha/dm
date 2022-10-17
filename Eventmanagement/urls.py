from django.urls import path 
from .views import *
urlpatterns = [
    path('',VenderoView.as_view()),
    path('event/',VendorEventView.as_view()),
    path('planner/',PlannerCategory.as_view()),
    path('like/',LikesView.as_view())
]
