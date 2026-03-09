from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Skill(models.model):
    name = models.CharField(max_length=200)

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)

class UserSkill(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Slot(models.Model):
    user_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE)
    slot_date = models.DateField(auto_now=False, default=date.today)

class Booking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    booker_user = models.ForeignKey(UserData, on_delete=models.CASCADE, default=0)
    is_booked = models.BooleanField(default=False)