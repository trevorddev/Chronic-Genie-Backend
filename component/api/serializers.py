from rest_framework import serializers
from component.models import (
    Food,
    Aggravator
) 

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        
        fields = '__all__'


class AggravatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aggravator
        
        fields = '__all__'
