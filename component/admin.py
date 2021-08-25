from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from component.models import Food



admin.site.register(Food)