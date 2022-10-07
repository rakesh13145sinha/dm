from rest_framework import serializers
from .models import *
class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model=Person 
        exclude=("active_plan","total_access")
