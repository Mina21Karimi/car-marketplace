from django.contrib import admin
from .models import CarListing, PartListing

@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model', 'year', 'price', 'status', 'created_at')
    list_filter = ('brand', 'status', 'year')
    search_fields = ('title', 'brand', 'model')

@admin.register(PartListing)
class PartListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'condition', 'price', 'created_at')
    list_filter = ('brand', 'condition')
    search_fields = ('name', 'brand', 'part_number')

from .models import CarListing, PartListing, Message, ConsultationRequest # ConsultationRequest اضافه شود

# ... کدهای قبلی ...

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'subject')
