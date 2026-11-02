from django.contrib import admin
from .models import CarListing, PartListing
from .models import CarListing, PartListing, Message, ConsultationRequest, Ticket, Dealership, SiteSetting, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model', 'year', 'price', 'status', 'created_at')
    list_filter = ('brand', 'status', 'year')
    search_fields = ('title', 'brand', 'model')
    inlines = [CarImageInline]

@admin.register(PartListing)
class PartListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'condition', 'price', 'created_at')
    list_filter = ('brand', 'condition')
    search_fields = ('name', 'brand', 'part_number')
@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'subject')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'category', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('subject', 'message', 'user__username')

@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'working_hours')
    search_fields = ('name', 'city', 'address')

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('eitaa_link', 'contact_phone')

    # جلوگیری از ساخت بیش از یک رکورد تنظیمات
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

