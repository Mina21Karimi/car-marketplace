from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/add/', views.add_car, name='add_car'),
    path('parts/add/', views.add_part, name='add_part'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cars/<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:pk>/delete/', views.delete_car, name='delete_car'),
    path('parts/<int:pk>/edit/', views.edit_part, name='edit_part'),
    path('parts/<int:pk>/delete/', views.delete_part, name='delete_part'),
    path('consultation/', views.consultation, name='consultation'),
    path('support/', views.submit_ticket, name='submit_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('management/', views.staff_dashboard, name='staff_dashboard'),
    path('dealerships/', views.dealerships, name='dealerships'),
    path('cars/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('cars/', views.all_cars, name='all_cars'), # <--- مسیر همه خودروها
    path('parts/<int:pk>/', views.part_detail, name='part_detail'),
]
