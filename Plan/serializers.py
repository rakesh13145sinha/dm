from rest_framework import serializers 
from .models import * 

class PlanSerializer(serializers.ModelSerializer):
    plan_detail=serializers.SerializerMethodField()
    
    def get_plan_detail(self,obj):
        fetures=obj.planfeature_set.all().order_by('priority')
        return [{"title":i.title,"image":i.image.url if i.image else None} for i in fetures ] 
    class Meta:
        model=MemberShip
        fields=["id","subscription",'discount','price','plan_detail']
        
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemberShip
        exclude=('created','status')
        
        

        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields='__all__'
        