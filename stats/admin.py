from django.contrib import admin

from .models import (
	daily_report,
	daily_report_food,
	daily_report_aggravator,
	daily_report_symptom,
	daily_report_comorbidity,
	daily_report_flare_medication
)
# Register your models here.

admin.site.register(daily_report)
admin.site.register(daily_report_food)
admin.site.register(daily_report_aggravator)
admin.site.register(daily_report_symptom)
admin.site.register(daily_report_comorbidity)
admin.site.register(daily_report_flare_medication)
