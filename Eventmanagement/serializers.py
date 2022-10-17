from rest_framework import serializers 
from .models import * 

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=VentorEvent
        exclude=('likes',)