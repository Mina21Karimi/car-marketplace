from .models import SiteSetting

def site_settings(request):
    # گرفتن اولین (و تنها) رکورد تنظیمات
    settings = SiteSetting.objects.first()
    return {'site_settings': settings}
