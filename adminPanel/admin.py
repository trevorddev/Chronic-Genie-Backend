from django.contrib import admin
from adminPanel.models import (
    AppSettings,
    Food,
    Aggravator,
    Symptom,
    Comorbidity,
    DailyMedication,
    FlareMedication,
)
# Register your models here.


admin.site.register(AppSettings)
admin.site.register(Food)
admin.site.register(Aggravator)
admin.site.register(Symptom)
admin.site.register(Comorbidity)
admin.site.register(DailyMedication)
admin.site.register(FlareMedication)