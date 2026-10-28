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

# ... (کدهای قبلی) ...

@login_required(login_url='login')
def dashboard(request):
    # گرفتن آگهی‌های خودرو و قطعه‌ای که کاربر جاری ثبت کرده است
    user_cars = CarListing.objects.filter(user=request.user).order_by('-created_at')
    user_parts = PartListing.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'core/dashboard.html', {
        'user_cars': user_cars,
        'user_parts': user_parts
    })

@login_required(login_url='login')
def edit_car(request, pk):
    car = get_object_or_404(CarListing, pk=pk, user=request.user) # فقط صاحب آگهی می‌تواند ویرایش کند
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CarListingForm(instance=car)
    return render(request, 'core/add_car.html', {'form': form, 'edit_mode': True})

@login_required(login_url='login')
def delete_car(request, pk):
    car = get_object_or_404(CarListing, pk=pk, user=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('dashboard')
    return render(request, 'core/confirm_delete.html', {'object': car, 'type': 'خودرو'})

@login_required(login_url='login')
def edit_part(request, pk):
    part = get_object_or_404(PartListing, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PartListingForm(request.POST, request.FILES, instance=part)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PartListingForm(instance=part)
    return render(request, 'core/add_part.html', {'form': form, 'edit_mode': True})

@login_required(login_url='login')
def delete_part(request, pk):
    part = get_object_or_404(PartListing, pk=pk, user=request.user)
    if request.method == 'POST':
        part.delete()
        return redirect('dashboard')
    return render(request, 'core/confirm_delete.html', {'object': part, 'type': 'قطعه'})
from .forms import CarListingForm, PartListingForm, MessageForm, ConsultationForm # ConsultationForm اضافه شود

# ... کدهای قبلی ...

def consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/consultation.html', {'form': ConsultationForm(), 'success': True})
    else:
        form = ConsultationForm()

    return render(request, 'core/consultation.html', {'form': form})
