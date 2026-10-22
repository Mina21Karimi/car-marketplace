from django.db import models
from django.utils import timezone

class CarListing(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('sold', 'فروخته شده'),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان آگهی")
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
