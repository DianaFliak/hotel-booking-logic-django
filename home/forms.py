# forms.py
from django import forms
from .models import Hotel, HotelBooking, Amenities, HotelImages

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_price', 'description', 'amenities', 'room_count']
        widgets = {
            'amenities': forms.CheckboxSelectMultiple(),  # Відображення для ManyToMany поля
        }

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['hotel', 'user', 'start_date', 'end_date', 'booking_type']
        widgets = {
            'user': forms.Select(),  # Вибір користувача
            'hotel': forms.Select(),  # Вибір готелю
        }

class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        fields = ['amenity_name']  # Змінено на amenity_name
        widgets = {
            'amenity_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_amenity_name'}),
        }

class HotelImagesForm(forms.ModelForm):
    class Meta:
        model = HotelImages
        fields = ['hotel', 'images']