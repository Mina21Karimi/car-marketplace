from django import forms
from .models import CarListing

class CarListingForm(forms.ModelForm):
    class Meta:
        model = CarListing
        fields = ['title', 'brand', 'model', 'year', 'mileage', 'price', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن کلاس‌های Tailwind به تمام فیلدها
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'
            })

from django import forms
from .models import CarListing, PartListing # PartListing اضافه شود

# ... (کلاس CarListingForm را دست نزنید) ...

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

from .models import CarListing, PartListing, Message # Message اضافه شود

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'پیام خود را بنویسید...', 'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary focus:border-primary dark:bg-gray-700 dark:text-white'})
        }

from .models import CarListing, PartListing, Message, ConsultationRequest # ConsultationRequest اضافه شود

# ... کدهای قبلی ...

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
