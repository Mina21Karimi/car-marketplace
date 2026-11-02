from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# ==========================================
# بخش خودروها و گالری تصاویر
# ==========================================
class CarListing(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('sold', 'فروخته شده'),
    )
    GEARBOX_TYPE_CHOICES = (
        ('manual', 'دنده‌ای'),
        ('automatic', 'اتوماتیک'),
    )
    ENGINE_STATUS_CHOICES = (
        ('healthy', 'سالم'),
        ('needs_repair', 'نیاز به تعمیر'),
        ('replaced', 'تعویض شده'),
    )
    GEARBOX_STATUS_CHOICES = (
        ('healthy', 'سالم'),
        ('needs_repair', 'نیاز به تعمیر'),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان آگهی")
    brand = models.CharField(max_length=100, verbose_name="برند")
    model = models.CharField(max_length=100, verbose_name="مدل")
    year = models.IntegerField(verbose_name="سال ساخت")
    mileage = models.IntegerField(verbose_name="کارکرد (کیلومتر)")
    city = models.CharField(max_length=100, verbose_name="شهر", default="تهران")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (تومان)")

    chassis_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="شاسی")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="رنگ")
    engine_status = models.CharField(max_length=50, choices=ENGINE_STATUS_CHOICES, default='healthy', verbose_name="وضعیت موتور")
    gearbox_type = models.CharField(max_length=50, choices=GEARBOX_TYPE_CHOICES, default='manual', verbose_name="نوع گیربکس")
    gearbox_status = models.CharField(max_length=50, choices=GEARBOX_STATUS_CHOICES, default='healthy', verbose_name="وضعیت گیربکس")
    is_exchangeable = models.BooleanField(default=False, verbose_name="امکان معاوضه")

    description = models.TextField(verbose_name="توضیحات")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published', verbose_name="وضعیت")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ثبت‌کننده", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return f"{self.brand} {self.model} - {self.year}"

    class Meta:
        verbose_name = "آگهی خودرو"
        verbose_name_plural = "آگهی‌های خودرو"


class CarImage(models.Model):
    car = models.ForeignKey(CarListing, related_name='images', on_delete=models.CASCADE, verbose_name="خودرو")
    image = models.ImageField(upload_to='cars/gallery/', verbose_name="تصویر")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تصویر خودرو"
        verbose_name_plural = "تصاویر خودرو (گالری)"

    def __str__(self):
        return f"تصویر برای {self.car.title}"


# ==========================================
# بخش قطعات یدکی
# ==========================================
class PartListing(models.Model):
    STATUS_CHOICES = (
        ('new', 'نو'),
        ('used', 'دست دوم'),
    )

    name = models.CharField(max_length=200, verbose_name="نام قطعه")
    brand = models.CharField(max_length=100, verbose_name="برند سازنده")
    part_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="شماره فنی قطعه")
    condition = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="وضعیت (نو/دست دوم)")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (تومان)")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='parts/', blank=True, null=True, verbose_name="تصویر قطعه")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر ثبت‌کننده", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.name} - {self.brand}"

    class Meta:
        verbose_name = "آگهی قطعه"
        verbose_name_plural = "آگهی‌های قطعات"


# ==========================================
# بخش پیام‌رسانی
# ==========================================
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


# ==========================================
# بخش درخواست مشاوره
# ==========================================
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


# ==========================================
# بخش پشتیبانی (تیکت)
# ==========================================
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


# ==========================================
# بخش نمایشگاه‌ها
# ==========================================
class Dealership(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام نمایشگاه")
    city = models.CharField(max_length=100, verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس دقیق")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    working_hours = models.CharField(max_length=100, verbose_name="ساعات کاری", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        verbose_name = "نمایشگاه خودرو"
        verbose_name_plural = "نمایشگاه‌های خودرو"


# ==========================================
# بخش تنظیمات سایت (لینک ایتا و ...)
# ==========================================
class SiteSetting(models.Model):
    eitaa_link = models.URLField(verbose_name="لینک کانال ایتا", blank=True, null=True, help_text="لینک کامل کانال ایتا را وارد کنید (مثلاً https://eitaa.com/your_channel)")
    contact_phone = models.CharField(max_length=20, verbose_name="شماره تماس پشتیبانی", blank=True, null=True)
    contact_email = models.EmailField(verbose_name="ایمیل پشتیبانی", blank=True, null=True)

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"


# ==========================================
# بخش علاقه‌مندی‌ها (Wishlist)
# ==========================================
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="کاربر")
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE, null=True, blank=True, verbose_name="خودرو")
    part = models.ForeignKey(PartListing, on_delete=models.CASCADE, null=True, blank=True, verbose_name="قطعه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ذخیره")

    class Meta:
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"

class Report(models.Model):
    REASON_CHOICES = (
        ('fake', 'آگهی جعلی یا کلاهبرداری'),
        ('wrong_info', 'اطلاعات نادرست'),
        ('sold', 'قبلاً فروخته شده'),
        ('other', 'سایر موارد'),
    )
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made', verbose_name="گزارش‌دهنده")
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE, null=True, blank=True, verbose_name="خودرو")
    part = models.ForeignKey(PartListing, on_delete=models.CASCADE, null=True, blank=True, verbose_name="قطعه")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name="دلیل گزارش")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات بیشتر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    is_reviewed = models.BooleanField(default=False, verbose_name="بررسی شده")

    class Meta:
        verbose_name = "گزارش تخلف"
        verbose_name_plural = "گزارش‌های تخلف"

    def __str__(self):
        return f"گزارش {self.get_reason_display()} - توسط {self.reporter.username}"
