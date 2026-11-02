from django import forms
from .models import CarListing, PartListing, Message, ConsultationRequest, Ticket, Report
from django.contrib.auth.models import User

# ==========================================
# ویجت سفارشی برای آپلود چند فایل (حل مشکل جنگو)
# ==========================================
class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# ==========================================
# فرم ثبت آگهی خودرو
# ==========================================
class CarListingForm(forms.ModelForm):
    # استفاده از فیلد سفارشی برای گالری
    gallery_images = MultipleFileField(
        widget=MultipleFileInput(attrs={
            'multiple': True,
            'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
        }),
        required=False,
        label="گالری تصاویر (حداکثر ۷ عکس)",
        help_text="می‌توانید با نگه داشتن کلید Ctrl، چند عکس را همزمان انتخاب کنید."
    )

    class Meta:
        model = CarListing
        fields = [
            'title', 'brand', 'model', 'year', 'mileage','city', 'price',
            'chassis_number', 'color', 'engine_status', 'gearbox_type',
            'gearbox_status', 'is_exchangeable', 'description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_exchangeable':
                field.widget.attrs.update({
                    'class': 'w-5 h-5 text-primary bg-gray-100 border-gray-300 rounded focus:ring-primary dark:focus:ring-primary dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
                })
            elif field_name != 'gallery_images':
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
                })

# ==========================================
# فرم ثبت آگهی قطعه
# ==========================================
class PartListingForm(forms.ModelForm):
    class Meta:
        model = PartListing
        fields = ['name', 'brand', 'part_number', 'condition', 'price', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            })

# ==========================================
# فرم پیام
# ==========================================
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'پیام خود را بنویسید...', 'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'})
        }

# ==========================================
# فرم مشاوره
# ==========================================
class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['name', 'phone', 'subject', 'budget', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            })

# ==========================================
# فرم تیکت پشتیبانی
# ==========================================
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'category', 'priority', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            })

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            })

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            })
