from django.shortcuts import render, redirect, get_object_or_404 # get_object_or_404 اضافه شد
from django.contrib.auth.decorators import login_required
from .models import CarListing, PartListing
from .forms import CarListingForm, PartListingForm
from django.db.models import Q # برای جستجوی پیشرفته

def home(request):
    query = request.GET.get('q') # دریافت عبارت جستجو از URL

    cars = CarListing.objects.filter(status='published')
    parts = PartListing.objects.all()

    if query:
        # جستجو در عنوان، برند و مدل خودرو
        cars = cars.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )
        # جستجو در نام و برند قطعات
        parts = parts.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query)
        )

    cars = cars.order_by('-created_at')[:6]
    parts = parts.order_by('-created_at')[:6]

    context = {
        'cars': cars,
        'parts': parts,
        'query': query, # ارسال عبارت جستجو به قالب
    }
    return render(request, 'core/index.html', context)

def car_detail(request, pk):
    # گرفتن آگهی بر اساس شناسه (id)، اگر پیدا نشد خطای 404 می‌دهد
    car = get_object_or_404(CarListing, pk=pk)
    return render(request, 'core/car_detail.html', {'car': car})

# ... (توابع add_car و add_part را دست نزنید، همان‌طور که هستند بمانند) ...

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

from .forms import CarListingForm, PartListingForm # PartListingForm اضافه شود

@login_required(login_url='login')
def add_part(request):
    if request.method == 'POST':
        form = PartListingForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save(commit=False)
            part.user = request.user
            part.save()
            return redirect('home')
    else:
        form = PartListingForm()

    return render(request, 'core/add_part.html', {'form': form})
