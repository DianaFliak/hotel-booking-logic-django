from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User
from . models import *
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, HotelBooking, Amenities, HotelImages
from .forms import HotelForm, HotelBookingForm, AmenitiesForm, HotelImagesForm  # Імпортуйте ваші форми
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import HotelImagesForm  # Імпортуйте форму для зображень готелів





def check_booking(uid, room_count, start_date, end_date):
    qs = HotelBooking.objects.filter(hotel__uid=uid)
    # qs1 = qs.filter(
    #     start_date__gte=start_date,
    #     end_date__lte=end_date,
    # )
    # qs2 = qs.filter(
    #     start_date__lte=start_date,
    #     end_date__gte=end_date,
    # )

    qs = qs.filter(
        Q(start_date__gte=start_date,
          end_date__lte=end_date)
        | Q(start_date__lte=start_date,
            end_date__gte=end_date)
    )
    # qs = qs1|qs2

    if len(qs) >= room_count:
        return False
    return True


def index(request):
    amenities = Amenities.objects.all()
    hotels = Hotel.objects.all()
    total_hotels = len(hotels)  
    selected_amenities = request.GET.getlist('selectAmenity')
    sort_by = request.GET.get('sortSelect')
    search = request.GET.get('searchInput')
    startdate = request.GET.get('startDate')
    enddate = request.GET.get('endDate')
    price = request.GET.get('price')

    if selected_amenities != []:
        hotels = hotels.filter(
            amenities__amenity_name__in=selected_amenities).distinct()
    if search:

        hotels = hotels.filter(Q(hotel_name__icontains=search)
                               | Q(description__icontains=search) | Q(amenities__amenity_name__contains=search))
        

    if sort_by:

        if sort_by == 'low_to_high':
            hotels = hotels.order_by('hotel_price')

        elif sort_by == 'high_to_low':
            hotels = hotels.order_by('-hotel_price')
    if price:

        hotels = hotels.filter(hotel_price__lte=int(price))

    if startdate and enddate:

        unbooked_hotels = []
        for i in hotels:
            valid = check_booking(i.uid, i.room_count, startdate, enddate)
            if valid:
                unbooked_hotels.append(i)
        hotels = unbooked_hotels
    hotels = hotels.distinct ()
    p = Paginator(hotels, 2)
    page_no = request.GET.get('page')

    hotels = p.get_page(1)

    if page_no:
        hotels = p.get_page(page_no)
    no_of_pages = list(range(1, p.num_pages+1))

    date = datetime.today().strftime('%Y-%m-%d')

    context = {'amenities': amenities, 'hotels': hotels, 'sort_by': sort_by,
               'search': search, 'selected_amenities': selected_amenities, 'no_of_pages': no_of_pages, 'max_price': price, 'startdate': startdate, "enddate": enddate, "date": date,'total_hotels':total_hotels}
    return render(request, 'home/index.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Аутентифікація користувача
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Якщо аутентифікація успішна, увійдіть в систему
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                # Якщо користувач неактивний
                messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            # Якщо аутентифікація не вдалася
            messages.error(request, "Invalid username or password. Please try again.")
    
    # Повертаємо форму для GET запиту або якщо аутентифікація не вдалася
    return render(request, 'home/signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Перевірка наявності імені користувача або пошти
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return redirect('signup')

        # Створення користувача з хешуванням пароля
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        messages.success(request, 'Welcome, signup successful! Please login.')
        return redirect('signin')

    return render(request, 'home/signup.html')


def signout(request):
    logout(request)
    return redirect('/')


def get_hotel(request, uid):
    hotel = Hotel.objects.get(uid=uid)
    context = {'hotel': hotel}
    context['date'] = datetime.today().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        checkin = request.POST.get('startDate')
        checkout = request.POST.get('endDate')
        context['startdate'] = checkin
        context['enddate'] = checkout

        try:
            valid = check_booking(
                hotel.uid, hotel.room_count, checkin, checkout)
            if not valid:
                messages.error(request, 'Booking for these days are full')
                return render(request, 'home/hotel.html', context)
        except:
            messages.error(request, 'Please Enter Valid Date Data')
            return render(request, 'home/hotel.html', context)
        HotelBooking.objects.create(hotel=hotel, user=request.user, start_date=checkin,
                                    end_date=checkout, booking_type='Pre Paid')
        messages.success(
            request, f'{hotel.hotel_name} Booked successfully your booking id is {HotelBooking.uid}.')
        return render(request, 'home/hotel.html', context)
    return render(request, 'home/hotel.html', context)

    
def about_us(request):
    return render(request, 'home/about_us.html')


# Перевірка, чи користувач є стаффом
def is_staff_user(user):
    return user.is_staff


@user_passes_test(is_staff_user)  # Доступ тільки для staff
def admin_dashboard(request):
    hotels = Hotel.objects.all()
    bookings = HotelBooking.objects.all()
    amenities = Amenities.objects.all()
    hotel_images = HotelImages.objects.all()

    if request.method == 'POST':
        # Обробка форм для додавання нових даних
        if 'hotel_form' in request.POST:
            hotel_form = HotelForm(request.POST)
            if hotel_form.is_valid():
                hotel_form.save()
                messages.success(request, 'Готель успішно додано!')
                return redirect('home/admin_dashboard')
        elif 'booking_form' in request.POST:
            booking_form = HotelBookingForm(request.POST)
            if booking_form.is_valid():
                booking_form.save()
                messages.success(request, 'Бронювання успішно додано!')
                return redirect('home/admin_dashboard')
        elif 'amenities_form' in request.POST:
            amenities_form = AmenitiesForm(request.POST)
            if amenities_form.is_valid():
                amenities_form.save()
                messages.success(request, 'Зручність успішно додано!')
                return redirect('home/admin_dashboard')
        elif 'hotel_images_form' in request.POST:
            hotel_images_form = HotelImagesForm(request.POST, request.FILES)
            if hotel_images_form.is_valid():
                hotel_images_form.save()
                messages.success(request, 'Зображення готелю успішно додано!')
                return redirect('home/admin_dashboard')
    else:
        hotel_form = HotelForm()
        booking_form = HotelBookingForm()
        amenities_form = AmenitiesForm()
        hotel_images_form = HotelImagesForm()

    context = {
        'hotels': hotels,
        'bookings': bookings,
        'amenities': amenities,
        'hotel_images': hotel_images,
        'hotel_form': hotel_form,
        'booking_form': booking_form,
        'amenities_form': amenities_form,
        'hotel_images_form': hotel_images_form,
    }
    return render(request, 'home/admin_dashboard.html', context)

@login_required
def manage_data(request):
    hotels = Hotel.objects.all()
    bookings = HotelBooking.objects.all()
    amenities = Amenities.objects.all()
    hotel_images = HotelImages.objects.all()

    if request.method == 'POST':
        # Handle form submissions for adding new data
        if 'hotel_form' in request.POST:
            hotel_form = HotelForm(request.POST)
            if hotel_form.is_valid():
                hotel_form.save()
                messages.success(request, 'Hotel added successfully!')
                return redirect('manage_data')
        elif 'booking_form' in request.POST:
            booking_form = HotelBookingForm(request.POST)
            if booking_form.is_valid():
                booking_form.save()
                messages.success(request, 'Booking added successfully!')
                return redirect('manage_data')
        elif 'amenities_form' in request.POST:
            amenities_form = AmenitiesForm(request.POST)
            if amenities_form.is_valid():
                amenities_form.save()
                messages.success(request, 'Amenity added successfully!')
                return redirect('manage_data')
        elif 'hotel_images_form' in request.POST:
            hotel_images_form = HotelImagesForm(request.POST, request.FILES)
            if hotel_images_form.is_valid():
                hotel_images_form.save()
                messages.success(request, 'Hotel image added successfully!')
                return redirect('manage_data')
    else:
        hotel_form = HotelForm()
        booking_form = HotelBookingForm()
        amenities_form = AmenitiesForm()
        hotel_images_form = HotelImagesForm()

    context = {
        'hotels': hotels,
        'bookings': bookings,
        'amenities': amenities,
        'hotel_images': hotel_images,
        'hotel_form': hotel_form,
        'booking_form': booking_form,
        'amenities_form': amenities_form,
        'hotel_images_form': hotel_images_form,
    }
    return render(request, 'home/admin_dashboard.html', context)

    
def hotel_update(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('manage_data')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'home/hotel_form.html', {'form': form})

def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        hotel.delete()
        return redirect('manage_data')
    return render(request, 'home/hotel_confirm_delete.html', {'hotel': hotel})

def booking_update(request, pk):
    booking = get_object_or_404(HotelBooking, pk=pk)
    if request.method == 'POST':
        form = HotelBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('manage_data')
    else:
        form = HotelBookingForm(instance=booking)
    return render(request, 'home/booking_form.html', {'form': form})

def booking_delete(request, pk):
    booking = get_object_or_404(HotelBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('manage_data')
    return render(request, 'home/booking_confirm_delete.html', {'booking': booking})

def amenities_update(request, pk):
    amenity = get_object_or_404(Amenities, pk=pk)
    if request.method == 'POST':
        form = AmenitiesForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('manage_data')
    else:
        form = AmenitiesForm(instance=amenity)
    return render(request, 'home/amenities_form.html', {'form': form})

def amenities_delete(request, pk):
    amenity = get_object_or_404(Amenities, pk=pk)
    if request.method == 'POST':
        amenity.delete()
        return redirect('manage_data')
    return render(request, 'home/amenities_confirm_delete.html', {'amenity': amenity})

def hotel_images_delete(request, pk):
    hotel_image = get_object_or_404(HotelImages, pk=pk)
    if request.method == 'POST':
        hotel_image.delete()
        return redirect('manage_data')
    return render(request, 'home/hotel_image_confirm_delete.html', {'hotel_image': hotel_image})

def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Перенаправлення на адмінську панель
    else:
        form = HotelForm()
    return render(request, 'home/hotel_create.html', {'form': form})


def booking_create(request):
    if request.method == 'POST':
        form = HotelBookingForm(request.POST)  # Використовуйте HotelBookingForm
        if form.is_valid():
            form.save()  # Зберігаємо бронювання
            return redirect('admin_dashboard')  # Перенаправлення на адмінську панель
    else:
        form = HotelBookingForm()  # Створюємо нову форму

    return render(request, 'home/booking_create.html', {'form': form})

def amenities_create(request):
    if request.method == 'POST':
        form = AmenitiesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Перенаправлення на адмінську панель
    else:
        form = AmenitiesForm()
    return render(request, 'home/amenities_create.html', {'form': form})

def hotel_images_create(request):
    if request.method == 'POST':
        form = HotelImagesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Перенаправлення на адмінську панель
    else:
        form = HotelImagesForm()
    return render(request, 'home/hotel_images_create.html', {'form': form})

def hotel_images_update(request, pk):
    hotel_image = get_object_or_404(HotelImages, pk=pk)  # Використовуйте HotelImages
    if request.method == 'POST':
        form = HotelImagesForm(request.POST, request.FILES, instance=hotel_image)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Перенаправлення на адмінську панель
    else:
        form = HotelImagesForm(instance=hotel_image)
    return render(request, 'home/hotel_image_form.html', {'form': form})