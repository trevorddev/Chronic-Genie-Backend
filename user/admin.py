from django.contrib import admin
import csv
from django.http import HttpResponse
from rangefilter.filters import DateRangeFilter


from django.contrib.auth.admin import UserAdmin
from user.models import Account


@admin.action(description='Export to CSV')
def export_as_csv(modeladmin, request, queryset):

	meta = modeladmin.model._meta
	field_names = [field.name for field in meta.fields]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
	writer = csv.writer(response)

	
	writer.writerow(["Email", "First Name", "D.O.B", "Gender", "Date Joined"])
	for s in queryset:
		writer.writerow([s.email, s.first_name, s.date_of_birth, s.gender, s.date_joined])
	return response


class AccountAdmin(UserAdmin):
	list_display = ('email', 'first_name', 'date_of_birth', 'gender', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', 'first_name',)
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = (('date_joined', DateRangeFilter), 'gender', 'last_login')
	fieldsets = ()
	ordering = ('date_joined',)

	actions = [export_as_csv]

admin.site.register(Account, AccountAdmin)