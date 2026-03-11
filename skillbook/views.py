from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import date
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from skillbook.models import Booking, Slot, Skill, UserSkill

# ///////////////////// Booked slots ////////////////////////////////////

def list_booked_slots(request: HttpRequest) -> HttpResponse:
    """ Vue : index / booked_list
    Affiche la liste des ressources prêtes à être 'bouquées'. """
    bookings = Booking.objects.filter(is_booked=True)
    return render(request, 'skillbook/booked_list.html', {'bookings': bookings})

# ///////////////////// CRUD ////////////////////////////////////

@login_required
def get_my_bookings(request: HttpRequest) -> HttpResponse:
    user_bookings = Booking.objects.filter(booker_user=request.user, is_booked=True)
    return render(request, 'skillbook/my_bookings_list.html', {'bookings': user_bookings})

@login_required
def get_bookings(request: HttpRequest) -> HttpResponse:
    bookings = Booking.objects.all()
    return render(request, 'skillbook/slot_list.html', {'bookings': bookings})

@login_required
def add_booking(request: HttpRequest, booking_id: int) -> HttpResponse:
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method =='POST':
        try:
            booking.is_booked = True
            booking.booker_user = request.user

            # booking.full_clean()
            booking.save()

            messages.success(request, "Booking successful !")
        except Exception as e:
            list_msg: list[str] = []

            if isinstance(e, ValidationError):
                if hasattr(e, 'message_dict') and e.message_dict:
                    dict_err: dict[str, list[str]] = e.message_dict
                    for msgs in dict_err.values():
                        list_msg.extend(msgs)
                elif hasattr(e, 'messages'):
                    list_msg.extend(e.messages)
            if list_msg:
                messages.error(request, " | ".join(list_msg))
            else:
                messages.error(request, str(e))
    return redirect('skillbook:slot_list')

@login_required
def cancel_booking(request: HttpRequest, booking_id: int) -> HttpResponse:
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method =='POST':
        try:
            booking.is_booked = False
            booking.booker_user = request.user

            booking.save()

            messages.success(request, "Booking canceled")
        except Exception as e:
            list_msg: list[str] = []

            if isinstance(e, ValidationError):
                if hasattr(e, 'message_dict') and e.message_dict:
                    dict_err: dict[str, list[str]] = e.message_dict
                    for msgs in dict_err.values():
                        list_msg.extend(msgs)
                elif hasattr(e, 'messages'):
                    list_msg.extend(e.messages)
            if list_msg:
                messages.error(request, " | ".join(list_msg))
            else:
                messages.error(request, str(e))
    return redirect('skillbook:slot_list')

@login_required
def get_all_skills(request: HttpRequest) -> HttpResponse:
    user_skills = UserSkill.objects.filter(user = request.user)
    skills = Skill.objects.exclude(pk__in=user_skills).order_by('name')
    return render(request, 'skillbook/skill_list.html', {'skills': skills, 'user_skills': user_skills})

@login_required
def add_skill(request: HttpRequest) -> HttpResponse:

    if request.method =='POST':
        try:
            new_skill = Skill(name=request.POST["name"])

            new_skill.save()

            messages.success(request, "Skill added successfully !")
        except Exception as e:
            list_msg: list[str] = []

            if isinstance(e, ValidationError):
                if hasattr(e, 'message_dict') and e.message_dict:
                    dict_err: dict[str, list[str]] = e.message_dict
                    for msgs in dict_err.values():
                        list_msg.extend(msgs)
                elif hasattr(e, 'messages'):
                    list_msg.extend(e.messages)
            if list_msg:
                messages.error(request, " | ".join(list_msg))
            else:
                messages.error(request, str(e))
    return redirect('skillbook:skill_list')

@login_required
def add_my_skill(request: HttpRequest, skill_id: int) -> HttpResponse:
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method =='POST':
        try:
            new_user_skill = UserSkill(user = request.user, skill = skill)

            new_user_skill.save()

            messages.success(request, "Skill added successfully !")
        except Exception as e:
            list_msg: list[str] = []

            if isinstance(e, ValidationError):
                if hasattr(e, 'message_dict') and e.message_dict:
                    dict_err: dict[str, list[str]] = e.message_dict
                    for msgs in dict_err.values():
                        list_msg.extend(msgs)
                elif hasattr(e, 'messages'):
                    list_msg.extend(e.messages)
            if list_msg:
                messages.error(request, " | ".join(list_msg))
            else:
                messages.error(request, str(e))
    return redirect('skillbook:skill_list')

@login_required
def remove_my_skill(request: HttpRequest, skill_id: int) -> HttpResponse:
    skill = get_object_or_404(Skill, id=skill_id)
    user_skill = get_object_or_404(UserSkill, skill = skill, user = request.user)

    if request.method =='POST':
        try:
            user_skill.delete()

            messages.success(request, "Skill remove from your list")
        except Exception as e:
            list_msg: list[str] = []

            if isinstance(e, ValidationError):
                if hasattr(e, 'message_dict') and e.message_dict:
                    dict_err: dict[str, list[str]] = e.message_dict
                    for msgs in dict_err.values():
                        list_msg.extend(msgs)
                elif hasattr(e, 'messages'):
                    list_msg.extend(e.messages)
            if list_msg:
                messages.error(request, " | ".join(list_msg))
            else:
                messages.error(request, str(e))
    return redirect('skillbook:skill_list')

@login_required
def get_my_skills(request: HttpRequest) -> HttpResponse:
    user_skills = UserSkill.objects.filter(user=request.user)
    return render(request, 'skillbook/my_skill_list.html', {'user_skills': user_skills})

@login_required
def add_slot(request: HttpRequest) -> HttpResponse:
    user_skills = UserSkill.objects.filter(user=request.user)
    return render(request, 'skillbook/add_slot.html', {'user_skills': user_skills})

@login_required
def propose_service(request: HttpRequest, skill_id: int):
    if request.method =='POST':
        try:
            user_skill = get_object_or_404(Skill, skill_id = skill_id, user = request.user)
            new_slot = Slot(user_skill,slot_date=request.POST["slot_date"])

            new_slot.save()

            messages.success(request, "Service added successfully !")
        except Exception as e:
            list_msg: list[str] = []

            if isinstance(e, ValidationError):
                if hasattr(e, 'message_dict') and e.message_dict:
                    dict_err: dict[str, list[str]] = e.message_dict
                    for msgs in dict_err.values():
                        list_msg.extend(msgs)
                elif hasattr(e, 'messages'):
                    list_msg.extend(e.messages)
            if list_msg:
                messages.error(request, " | ".join(list_msg))
            else:
                messages.error(request, str(e))
    return redirect('skillbook:booked_list')