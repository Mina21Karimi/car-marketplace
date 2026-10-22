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
