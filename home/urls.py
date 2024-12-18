"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from hotelProject import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('hotel/<uid>',get_hotel,name='get_hotel'),
    path('about/', about_us, name='about_us'),
    path('myadmin/dashboard/', admin_dashboard, name='admin_dashboard'),
    
    path('manage/', manage_data, name='manage_data'),

    path('hotel/update/<uuid:pk>/', hotel_update, name='hotel_update'),  #+
    path('hotel/delete/<uuid:pk>/', hotel_delete, name='hotel_delete'),  
    path('hotel/create/', hotel_create, name='hotel_create'), #+

    path('booking/update/<uuid:pk>/', booking_update, name='booking_update'),  #+
    path('booking/delete/<uuid:pk>/', booking_delete, name='booking_delete'),  
    path('booking/create/', booking_create, name='booking_create'),  #+

    path('amenities/update/<uuid:pk>/', amenities_update, name='amenities_update'),  #+
    path('amenities/delete/<uuid:pk>/', amenities_delete, name='amenities_delete'),
    path('amenities/create/', amenities_create, name='amenities_create'),  #+
  
    path('hotel_images/update/<uuid:pk>/', hotel_images_update, name='hotel_images_update'), #+ 
    path('hotel_images/delete/<uuid:pk>/', hotel_images_delete, name='hotel_images_delete'),  
    path('hotel_images/create/', hotel_images_create, name='hotel_images_create'), #+
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()