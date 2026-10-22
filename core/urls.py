from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/add/', views.add_car, name='add_car'), # <--- این خط اضافه شود
]
