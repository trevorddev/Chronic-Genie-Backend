from django.urls import path

from . import views

app_name = 'component'

urlpatterns = [
    path('foods', views.FoodRetrieveAll.as_view(), name = "food list"),
    path('food/<pk>', views.api_detail_update_delete_food_view, name="food detail"),
    path('food', views.api_create_food_view, name="food create")

]