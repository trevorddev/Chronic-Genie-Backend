from django.contrib import admin
import csv
from django.http import HttpResponse

from adminPanel.models import (
    AppSettings,
    Food,
    Aggravator,
    Symptom,
    Comorbidity,
    DailyMedication,
    FlareMedication,
    MarketingEmail
)
# Register your models here.

class AppSettingsAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True

@admin.action(description='Export to CSV')
def export_as_csv(modeladmin, request, queryset):

	meta = modeladmin.model._meta
	field_names = [field.name for field in meta.fields]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
	writer = csv.writer(response)

	
	writer.writerow(["Email", "is_subscribed"])
	for s in queryset:
		writer.writerow([s.email, s.is_subscribed])
	return response
class MarketingEmailAdmin(admin.ModelAdmin):
	list_display = ('email', 'is_subscribed')
	search_fields = ('email',)

	filter_horizontal = ()
	list_filter = ('is_subscribed',)
	fieldsets = ()
	ordering = ('email',)

	actions = [export_as_csv]

admin.site.register(AppSettings, AppSettingsAdmin)
admin.site.register(Food)
admin.site.register(Aggravator)
admin.site.register(Symptom)
admin.site.register(Comorbidity)
admin.site.register(DailyMedication)
admin.site.register(FlareMedication)
admin.site.register(MarketingEmail, MarketingEmailAdmin)

# hiding site administration text from home page
admin.site.index_title = ''