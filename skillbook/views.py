from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from skillbook.models import Booking

# ///////////////////// Booked slots ////////////////////////////////////

def list_booked_slots(request: HttpRequest) -> HttpResponse:
    """ Vue : index / booked_list
    Affiche la liste des ressources prêtes à être 'bouquées'. """
    bookings = Booking.objects.all()
    return render(request, 'skillbook/booked_list.html', {'bookings': bookings})