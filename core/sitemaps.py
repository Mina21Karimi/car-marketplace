from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CarListing, PartListing

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'consultation', 'dealerships']

    def location(self, item):
        return reverse(item)

class CarSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return CarListing.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

class PartSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return PartListing.objects.all()

    def lastmod(self, obj):
        return obj.created_at
