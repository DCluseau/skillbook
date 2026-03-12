from datetime import date

from django.db import models
from django.contrib.auth.models import User
from typing import Any, Optional

from django.forms import ValidationError

class Skill(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.skill}"

class Slot(models.Model):
    user_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE)
    slot_date = models.DateField(auto_now=False, default=date.today)

    def __str__(self):
        return f"{self.user_skill} - {self.slot_date}"
    
    def save(self, *args: Any, **kwargs: Any) -> None:
            """
            Save method override to secure the data saving
            """
            self.full_clean()
            super().save(*args, **kwargs)
    
    def clean(self):
        # Check if the selected date does not precede today's date
        if self.slot_date < date.today():
              raise ValidationError("Slot's date can't be anterior to today's date.")

class Booking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    booker_user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slot} - {self.booker_user} - {self.is_booked}"
    
    def clean(self):
        # Check if the slot is being modified elsewhere
        # If so, raise an error
        conflicts = Booking.objects.filter(
                slot=self.slot,
                booker_user=self.booker_user,
                is_booked=self.is_booked,
            )
        if self.is_booked and self.booker_user == self.slot.user_skill.user.username:
             raise ValidationError("You can't book yourself.")
        if self.is_booked and self.booker_user != self.slot.user_skill.user.username:
            if self.pk:
                conflicts = conflicts.exclude(pk=self.pk)
            if conflicts.exists():
                conflict: Optional[Booking] = conflicts.first()
                if conflict:
                    raise ValidationError(
                        f"This slot is already booked."
                    )
    def save(self, *args: Any, **kwargs: Any) -> None:
            # Save method override to secure the data saving
            self.full_clean()
            super().save(*args, **kwargs)