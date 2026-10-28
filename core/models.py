from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CarListing(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('sold', 'فروخته شده'),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان آگهی")
    from django.contrib.auth.models import User # این خط را بالای فایل اضافه کنید

# ... (داخل کلاس CarListing)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ثبت‌کننده", null=True, blank=True)
    brand = models.CharField(max_length=100, verbose_name="برند")
    model = models.CharField(max_length=100, verbose_name="مدل")
    year = models.IntegerField(verbose_name="سال ساخت")
    mileage = models.IntegerField(verbose_name="کارکرد (کیلومتر)")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (تومان)")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="تصویر خودرو")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published', verbose_name="وضعیت")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return f"{self.brand} {self.model} - {self.year}"

    class Meta:
        verbose_name = "آگهی خودرو"
        verbose_name_plural = "آگهی‌های خودرو"


class PartListing(models.Model):
    STATUS_CHOICES = (
        ('new', 'نو'),
        ('used', 'دست دوم'),
    )
# داخل کلاس PartListing، بعد از خط name:
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ثبت‌کننده", null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name="نام قطعه")
    brand = models.CharField(max_length=100, verbose_name="برند سازنده")
    part_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="شماره فنی قطعه")
    condition = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="وضعیت (نو/دست دوم)")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (تومان)")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='parts/', blank=True, null=True, verbose_name="تصویر قطعه")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.name} - {self.brand}"

    class Meta:
        verbose_name = "آگهی قطعه"
        verbose_name_plural = "آگهی‌های قطعات"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="فرستنده")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="گیرنده")
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE, related_name='messages', verbose_name="درباره خودرو", null=True, blank=True)
    content = models.TextField(verbose_name="متن پیام")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ارسال")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")

    def __str__(self):
        return f"پیام از {self.sender.username} به {self.receiver.username}"

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"

class ConsultationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار بررسی'),
        ('contacted', 'تماس گرفته شده'),
        ('completed', 'انجام شده'),
    )

    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    subject = models.CharField(max_length=200, verbose_name="موضوع مشاوره")
    budget = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="بودجه تقریبی (تومان)", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات و نیازها")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت پیگیری")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"مشاوره: {self.name} - {self.subject}"

    class Meta:
        verbose_name = "درخواست مشاوره"
        verbose_name_plural = "درخواست‌های مشاوره"

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('open', 'باز'),
        ('in_progress', 'در حال بررسی'),
        ('closed', 'بسته شده'),
    )
    PRIORITY_CHOICES = (
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'زیاد'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', verbose_name="کاربر")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    category = models.CharField(max_length=100, verbose_name="دسته‌بندی (مثلاً مالی، فنی)")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="اولویت")
    message = models.TextField(verbose_name="متن پیام")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="وضعیت")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"تیکت {self.id}: {self.subject}"

    class Meta:
        verbose_name = "تیکت پشتیبانی"
        verbose_name_plural = "تیکت‌های پشتیبانی"
