from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/add/', views.add_car, name='add_car'),
    path('parts/add/', views.add_part, name='add_part'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('inbox/', views.inbox, name='inbox'),

       # مسیرهای جدید پنل کاربری
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cars/<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:pk>/delete/', views.delete_car, name='delete_car'),
    path('parts/<int:pk>/edit/', views.edit_part, name='edit_part'),
    path('parts/<int:pk>/delete/', views.delete_part, name='delete_part'),
    path('consultation/', views.consultation, name='consultation'),
]
