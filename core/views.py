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

from .forms import CarListingForm, PartListingForm, MessageForm # MessageForm اضافه شود

# تابع car_detail را با این جایگزین کنید:
def car_detail(request, pk):
    car = get_object_or_404(CarListing, pk=pk)
    message_form = MessageForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.receiver = car.user # فرستادن به ثبت‌کننده آگهی
            message.car = car
            message.save()
            return redirect('car_detail', pk=car.pk) # رفرش صفحه بعد از ارسال

    return render(request, 'core/car_detail.html', {'car': car, 'message_form': message_form})

@login_required(login_url='login')
def inbox(request):
    # گرفتن تمام پیام‌های دریافتی کاربر جاری
    messages = request.user.received_messages.all().order_by('-created_at')
    return render(request, 'core/inbox.html', {'messages': messages})

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
