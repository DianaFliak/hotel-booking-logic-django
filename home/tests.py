from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Hotel, HotelBooking, Amenities

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_can_sign_in(self):
        response = self.client.post(reverse('signin'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Перенаправлення після успішного входу
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_can_sign_up(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправлення після успішної реєстрації
        self.assertTrue(User.objects.filter(username='newuser').exists())

class HotelModelTests(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            hotel_name='Test Hotel',
            description='A nice place to stay',
            hotel_price=100,
            room_count=5
        )

    def test_hotel_creation(self):
        self.assertEqual(self.hotel.hotel_name, 'Test Hotel')
        self.assertEqual(self.hotel.hotel_price, 100)
        self.assertEqual(self.hotel.room_count, 5)

class HotelBookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.hotel = Hotel.objects.create(
            hotel_name='Test Hotel',
            description='A nice place to stay',
            hotel_price=100,
            room_count=5
        )

    def test_booking_creation(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('get_hotel', args=[self.hotel.uid]), {
            'startDate': '2023-10-01',
            'endDate': '2023-10-05'
        })
        self.assertEqual(response.status_code, 200)  # Перевірка, що сторінка завантажилася
        self.assertTrue(HotelBooking.objects.filter(user=self.user, hotel=self.hotel).exists())

class AmenitiesModelTests(TestCase):
    def setUp(self):
        self.amenity = Amenities.objects.create(amenity_name='Free Wi-Fi')

    def test_amenity_creation(self):
        self.assertEqual(self.amenity.amenity_name, 'Free Wi-Fi')

class IndexPageTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Перевірка, що сторінка завантажилася
        self.assertTemplateUsed(response, 'home/index.html')  # Перевірка, що використовується правильний шаблон
