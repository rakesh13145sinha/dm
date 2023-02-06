from django.urls import path 
from .views import * 
urlpatterns = [
    path('update',generate_request,name="send request for update profile"),
    path("update/status",update_request,name="update request status"),
    path('doc',DocumentVerify.as_view(),name="document_upload")
]
