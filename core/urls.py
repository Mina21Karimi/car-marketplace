from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/add/', views.add_car, name='add_car'),
    path('parts/add/', views.add_part, name='add_part'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'), # <--- این خط اضافه شود
]
