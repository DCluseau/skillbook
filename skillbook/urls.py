from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls.resolvers import URLPattern
from typing import List

app_name: str = 'skillbook'

urlpatterns: List[URLPattern] = [
    # Main page
    path('', views.list_booked_slots, name='booked_list'),
    # Slots list
    path('slot_list/', views.get_bookings, name='slot_list'),
    path('<int:booking_id>/add_booking/', views.add_booking, name='add_booking'),
    path('my_bookings_list/', views.get_my_bookings, name='my_bookings_list'),
    path('<int:booking_id>/cancel_booking/', views.cancel_booking, name='cancel_booking'),
    path('skill_list/', views.get_all_skills, name='get_all_skills'),
    path('<int:skill_id>/add_my_skill/', views.add_my_skill, name='add_my_skill'),
    path('<int:skill_id>/remove_my_skill/', views.remove_my_skill, name='remove_my_skill'),
]