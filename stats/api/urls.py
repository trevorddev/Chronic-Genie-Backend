from django.urls import path

from . import views

app_name = 'stats'

urlpatterns = [
    path('get_daily_report', views.get_daily_report, name="Get Daily Record"),
    path('add_daily_report', views.add_daily_report, name="Add Daily Record"),
    path('customized_search', views.customized_search, name="customized search"),
    path('user_dashboard', views.user_dashboard, name="user dashboard"),
    path('users_summary', views.users_summary, name="user summary")
]