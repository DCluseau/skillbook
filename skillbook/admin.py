from django.contrib import admin
from django import forms
from django.db.models.fields import Field
from django.http import HttpRequest
from typing import Any, Optional
from .models import Skill, Booking, UserSkill, Slot

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def formfield_for_dbfield(
        self,
        db_field: 'Field[Any, Any]',
        request: Optional[HttpRequest],
        **kwargs: Any
    ) -> Optional[forms.Field]:
        
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('skill',)
    search_fields = ('skill',)

    def formfield_for_dbfield(
        self,
        db_field: 'Field[Any, Any]',
        request: Optional[HttpRequest],
        **kwargs: Any
    ) -> Optional[forms.Field]:
        
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('user_skill', 'slot_date',)
    search_fields = ('user_skill', 'slot_date',)

    def formfield_for_dbfield(
        self,
        db_field: 'Field[Any, Any]',
        request: Optional[HttpRequest],
        **kwargs: Any
    ) -> Optional[forms.Field]:
        
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('slot', 'booker_user')
    list_filter = ('slot', 'booker_user')
    search_fields = ('slot__date', 'booker_user')