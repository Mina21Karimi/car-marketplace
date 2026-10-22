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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CarListing, PartListing
from .forms import CarListingForm
# (کدهای مربوط به تابع home را دست نزنید، فقط این را اضافه کنید)

@login_required(login_url='login')
def add_car(request):
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user # ثبت آگهی به نام کاربر لاگین شده
            car.save()
            return redirect('home')
    else:
        form = CarListingForm()

    return render(request, 'core/add_car.html', {'form': form})
