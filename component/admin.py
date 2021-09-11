from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from component.models import (
	AppSettings, 
	Food, 
	Aggravator, 
	Symptom, 
	Comorbidity, 
	DailyMedication, 
	FlareMedication,
)

class AppSettingsAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True

admin.site.register(AppSettings, AppSettingsAdmin)

# admin.site.register(Food)
# admin.site.register(Aggravator)
# admin.site.register(Symptom)
# admin.site.register(Comorbidity)
# admin.site.register(DailyMedication)
# admin.site.register(FlareMedication)