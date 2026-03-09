from django.urls import path
from . import views
from django.urls.resolvers import URLPattern
from typing import List

app_name: str = 'skillbook'

urlpatterns: List[URLPattern] = [
    # Main page
    path('', views.list_booked_slots, name='booked_list'),
]