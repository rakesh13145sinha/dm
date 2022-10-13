from rest_framework import serializers 
from .models import * 

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemberShip
        fields='__all__'
        
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemberShip
        exclude=('created','month','status')