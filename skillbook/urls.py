from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls.resolvers import URLPattern
from typing import List

app_name: str = 'skillbook'

urlpatterns: List[URLPattern] = [
    # Main page
    path('', views.list_booked_slots, name='booked_list'),
    # Main app pages
    path('slot_list/', views.get_bookings, name='slot_list'),
    path('<int:booking_id>/add_booking/', views.add_booking, name='add_booking'),
    path('my_bookings_list/', views.get_my_bookings, name='my_bookings_list'),
    path('<int:booking_id>/cancel_booking/', views.cancel_booking, name='cancel_booking'),
    path('skill_list/', views.get_all_skills, name='skill_list'),
    path('add_skill/', views.add_skill, name='add_skill'),
    path('<int:skill_id>/add_my_skill/', views.add_my_skill, name='add_my_skill'),
    path('<int:skill_id>/remove_my_skill/', views.remove_my_skill, name='remove_my_skill'),
    path('my_skill_list/', views.get_my_skills, name='my_skill_list'),
    path('add_slot/', views.add_slot, name='add_slot'),
    path('my_services/', views.my_services, name='my_services'),
    path('propose_service/', views.propose_service, name='propose_service'),
    path('<int:booking_id>/delete_service/', views.delete_service, name='delete_service'),
    path('<int:slot_id>/edit_service/', views.edit_service, name='edit_service'),
    path('<int:slot_id>/edit_my_slot/', views.edit_my_slot, name='edit_my_slot'),
]