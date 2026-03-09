from datetime import date

from django.db import models
from django.contrib.auth.models import User
from typing import Any

class Skill(models.model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.user} - {self.email}"

class UserSkill(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} - {self.skill}"

class Slot(models.Model):
    user_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE)
    slot_date = models.DateField(auto_now=False, default=date.today)

    def __str__(self):
        return f"{self.user_skill} - {self.slot_date}"
    
    def save(self, *args: Any, **kwargs: Any) -> None:
            """
            Surcharge du save pour sécuriser l'enregistrement.
            """
            self.full_clean()
            super().save(*args, **kwargs)

class Booking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    booker_user = models.ForeignKey(UserData, on_delete=models.CASCADE, default=0)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slot} - {self.booker_user} - {self.is_booked}"
    
    def save(self, *args: Any, **kwargs: Any) -> None:
            """
            Surcharge du save pour sécuriser l'enregistrement.
            """
            self.full_clean()
            super().save(*args, **kwargs)