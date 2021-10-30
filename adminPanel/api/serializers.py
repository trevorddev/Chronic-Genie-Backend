from rest_framework import serializers
from adminPanel.models import (
    Food,
    Aggravator,
    Symptom,
    Comorbidity,
    DailyMedication,
    FlareMedication,
    MarketingEmail
) 

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        
        fields = '__all__'


class AggravatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aggravator
        
        fields = '__all__'


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        
        fields = '__all__'

class ComorbiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comorbidity
        
        fields = '__all__'


class DailyMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMedication

        fields = '__all__'


class FlareMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlareMedication
        
        fields = '__all__'


class MarketingEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingEmail
        
        fields = '__all__'