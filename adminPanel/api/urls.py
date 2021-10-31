from django.urls import path

from . import views

app_name = 'adminPanel'

urlpatterns = [
    
    path('food/', views.FoodCreateRetrieve.as_view()),
    path('food/<pk>/', views.FoodAPIView.as_view()),
    
    path('aggravator/', views.AggravatorCreateRetrieve.as_view()),
    path('aggravator/<pk>/', views.AggravatorAPIView.as_view()),
    
    path('symptom/', views.SymptomCreateRetrieve.as_view()),
    path('symptom/<pk>/', views.SymptomAPIView.as_view()),
    
    path('comorbidity/', views.ComorbidityCreateRetrieve.as_view()),
    path('comorbidity/<pk>/', views.ComorbidityAPIView.as_view()),
    
    path('dailyMedication/', views.DailyMedicationCreateRetrieve.as_view()),
    path('dailyMedication/<pk>/', views.DailyMedicationAPIView.as_view()),
    
    path('flareMedication/', views.FlareMedicationCreateRetrieve.as_view()),
    path('flareMedication/<pk>/', views.FlareMedicationAPIView.as_view()),
    
    path('marketingEmail/', views.MarketingEmailRetrieve.as_view()),

    path('appSetting/', views.appSettingCreateRetrieve.as_view()),
    path('appSetting/<pk>/', views.appSettingAPIView.as_view()),
]