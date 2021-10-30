
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from adminPanel.models import (
	Food,
    Aggravator,
    Symptom,
    Comorbidity,
    DailyMedication,
    FlareMedication,
    MarketingEmail
)
from .serializers import(
    FoodSerializer,
    AggravatorSerializer,
    SymptomSerializer,
    ComorbiditySerializer,
    DailyMedicationSerializer,
    FlareMedicationSerializer,
    MarketingEmailSerializer
)


@permission_classes((IsAuthenticated, IsAdminUser))
class FoodAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

@permission_classes((IsAuthenticated, IsAdminUser))
class FoodCreateRetrieve(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer



@permission_classes((IsAuthenticated, IsAdminUser))
class AggravatorAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aggravator.objects.all()
    serializer_class = AggravatorSerializer

@permission_classes((IsAuthenticated, IsAdminUser))
class AggravatorCreateRetrieve(generics.ListCreateAPIView):
    queryset = Aggravator.objects.all()
    serializer_class = AggravatorSerializer



@permission_classes((IsAuthenticated, IsAdminUser))
class SymptomAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer

@permission_classes((IsAuthenticated, IsAdminUser))
class SymptomCreateRetrieve(generics.ListCreateAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer



@permission_classes((IsAuthenticated, IsAdminUser))
class ComorbidityAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comorbidity.objects.all()
    serializer_class = ComorbiditySerializer

@permission_classes((IsAuthenticated, IsAdminUser))
class ComorbidityCreateRetrieve(generics.ListCreateAPIView):
    queryset = Comorbidity.objects.all()
    serializer_class = ComorbiditySerializer



@permission_classes((IsAuthenticated, IsAdminUser))
class DailyMedicationAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DailyMedication.objects.all()
    serializer_class = DailyMedicationSerializer

@permission_classes((IsAuthenticated, IsAdminUser))
class DailyMedicationCreateRetrieve(generics.ListCreateAPIView):
    queryset = DailyMedication.objects.all()
    serializer_class = DailyMedicationSerializer



@permission_classes((IsAuthenticated, IsAdminUser))
class FlareMedicationAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlareMedication.objects.all()
    serializer_class = FlareMedicationSerializer

@permission_classes((IsAuthenticated, IsAdminUser))
class FlareMedicationCreateRetrieve(generics.ListCreateAPIView):
    queryset = FlareMedication.objects.all()
    serializer_class = FlareMedicationSerializer


@permission_classes((IsAuthenticated, IsAdminUser))
class MarketingEmailRetrieve(generics.ListAPIView):
    queryset = MarketingEmail.objects.all()
    serializer_class = MarketingEmailSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'is_subscribed']
