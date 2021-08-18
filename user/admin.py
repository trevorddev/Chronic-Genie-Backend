from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import Account


class AccountAdmin(UserAdmin):
	list_display = ('email', 'first_name', 'date_of_birth', 'gender', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', 'first_name',)
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	ordering = ('email',)

admin.site.register(Account, AccountAdmin)