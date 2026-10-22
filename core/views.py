from django.shortcuts import render
from .models import CarListing, PartListing

def home(request):
    # گرفتن ۶ آگهی خودرو و ۶ آگهی قطعه آخر
    cars = CarListing.objects.filter(status='published').order_by('-created_at')[:6]
    parts = PartListing.objects.all().order_by('-created_at')[:6]

    context = {
        'cars': cars,
        'parts': parts,
    }
    return render(request, 'core/index.html', context)
