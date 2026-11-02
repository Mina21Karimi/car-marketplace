from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .models import (
    CarListing, PartListing, Message, ConsultationRequest,
    Ticket, Dealership, SiteSetting, Favorite, CarImage, Report
)
from .forms import (
    CarListingForm, PartListingForm, MessageForm,
    ConsultationForm, TicketForm, UserProfileForm, ReportForm
)
from django.core.paginator import Paginator

# ==========================================
# بخش صفحه اصلی و جستجو
# ==========================================
def home(request):
    query = request.GET.get('q', '')
    cars = CarListing.objects.filter(status='published')
    parts = PartListing.objects.all()

    if query:
        cars = cars.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )
        parts = parts.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query)
        )

    cars = cars.order_by('-created_at')[:6]
    parts = parts.order_by('-created_at')[:6]

    context = {
        'cars': cars,
        'parts': parts,
        'query': query,
    }
    return render(request, 'core/index.html', context)

# ==========================================
# بخش خودروها (نمایش، ثبت، ویرایش، حذف)
# ==========================================
def car_detail(request, pk):
    car = get_object_or_404(CarListing, pk=pk)
    message_form = MessageForm()

    # بررسی وضعیت علاقه‌مندی کاربر
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, car=car).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.receiver = car.user
            message.car = car
            message.save()
            return redirect('car_detail', pk=car.pk)

    return render(request, 'core/car_detail.html', {
        'car': car,
        'message_form': message_form,
        'is_favorite': is_favorite
    })

@login_required(login_url='login')
def add_car(request):
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()

            # گرفتن و ذخیره عکس‌های گالری (حداکثر ۷ عدد)
            images = request.FILES.getlist('gallery_images')
            for img in images[:7]:
                CarImage.objects.create(car=car, image=img)

            return redirect('home')
    else:
        form = CarListingForm()
    return render(request, 'core/add_car.html', {'form': form})

@login_required(login_url='login')
def edit_car(request, pk):
    car = get_object_or_404(CarListing, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()

            # اگر در حالت ویرایش عکس جدید آپلود شد، به گالری اضافه کن
            new_images = request.FILES.getlist('gallery_images')
            # بررسی کنیم مجموع عکس‌ها بیشتر از ۷ نشود
            current_count = car.images.count()
            for img in new_images:
                if current_count < 7:
                    CarImage.objects.create(car=car, image=img)
                    current_count += 1

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

# ==========================================
# بخش قطعات (ثبت، ویرایش، حذف)
# ==========================================
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

# ==========================================
# بخش پنل کاربری و پیام‌ها
# ==========================================
@login_required(login_url='login')
def dashboard(request):
    user_cars = CarListing.objects.filter(user=request.user).order_by('-created_at')
    user_parts = PartListing.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {
        'user_cars': user_cars,
        'user_parts': user_parts
    })

@login_required(login_url='login')
def inbox(request):
    messages = request.user.received_messages.all().order_by('-created_at')
    return render(request, 'core/inbox.html', {'messages': messages})

# ==========================================
# بخش علاقه‌مندی‌ها (Wishlist)
# ==========================================
@login_required(login_url='login')
def toggle_favorite(request, pk):
    car = get_object_or_404(CarListing, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)

    if not created:
        favorite.delete()

    return redirect('car_detail', pk=car.pk)

@login_required(login_url='login')
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_favorites.html', {'favorites': favorites})

# ==========================================
# بخش مشاوره و پشتیبانی
# ==========================================
def consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/consultation.html', {'form': ConsultationForm(), 'success': True})
    else:
        form = ConsultationForm()
    return render(request, 'core/consultation.html', {'form': form})

@login_required(login_url='login')
def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return render(request, 'core/support.html', {'form': TicketForm(), 'success': True})
    else:
        form = TicketForm()
    return render(request, 'core/support.html', {'form': form})

@login_required(login_url='login')
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_tickets.html', {'tickets': tickets})

# ==========================================
# بخش مدیریت، نمایشگاه‌ها و تنظیمات
# ==========================================
@login_required(login_url='login')
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    total_users = User.objects.count()
    total_cars = CarListing.objects.count()
    total_parts = PartListing.objects.count()
    open_tickets = Ticket.objects.filter(status='open').count()
    total_consultations = ConsultationRequest.objects.count()

    recent_cars = CarListing.objects.order_by('-created_at')[:5]
    recent_tickets = Ticket.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'total_cars': total_cars,
        'total_parts': total_parts,
        'open_tickets': open_tickets,
        'total_consultations': total_consultations,
        'recent_cars': recent_cars,
        'recent_tickets': recent_tickets,
    }
    return render(request, 'core/staff_dashboard.html', context)

def dealerships(request):
    all_dealerships = Dealership.objects.all().order_by('-created_at')
    return render(request, 'core/dealerships.html', {'dealerships': all_dealerships})

def all_cars(request):
    cars_list = CarListing.objects.filter(status='published').order_by('-created_at')

    # دریافت مقادیر فیلترها از URL
    q = request.GET.get('q')
    city = request.GET.get('city')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    year = request.GET.get('year')
    gearbox = request.GET.get('gearbox')

    # اعمال فیلترها
    if q:
        cars_list = cars_list.filter(Q(title__icontains=q) | Q(brand__icontains=q) | Q(model__icontains=q))
    if city:
        cars_list = cars_list.filter(city__icontains=city)
    if brand:
        cars_list = cars_list.filter(brand__icontains=brand)
    if min_price:
        cars_list = cars_list.filter(price__gte=min_price)
    if max_price:
        cars_list = cars_list.filter(price__lte=max_price)
    if year:
        cars_list = cars_list.filter(year__gte=year)
    if gearbox:
        cars_list = cars_list.filter(gearbox_type=gearbox)

    # صفحه‌بندی
    paginator = Paginator(cars_list, 12)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)

    return render(request, 'core/all_cars.html', {'cars': cars})

def part_detail(request, pk):
    part = get_object_or_404(PartListing, pk=pk)
    return render(request, 'core/part_detail.html', {'part': part})

@login_required(login_url='login')
def mark_as_sold(request, pk):
    car = get_object_or_404(CarListing, pk=pk, user=request.user)
    if request.method == 'POST':
        car.status = 'sold'
        car.save()
    return redirect('dashboard')

@login_required(login_url='login')
def profile_settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'core/profile_settings.html', {'form': form})

@login_required(login_url='login')
def report_car(request, pk):
    car = get_object_or_404(CarListing, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.car = car
            report.save()
            return render(request, 'core/report_success.html')
    else:
        form = ReportForm()
    return render(request, 'core/report_car.html', {'form': form, 'car': car})

def seller_profile(request, user_id):
    seller = get_object_or_404(User, pk=user_id)
    # گرفتن تمام آگهی‌های منتشرشده این فروشنده
    cars = CarListing.objects.filter(user=seller, status='published').order_by('-created_at')
    parts = PartListing.objects.filter(user=seller).order_by('-created_at')

    return render(request, 'core/seller_profile.html', {
        'seller': seller,
        'cars': cars,
        'parts': parts
    })
