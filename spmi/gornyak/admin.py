from django.contrib import admin
from .models import Event , EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'sport_type', 'organizer', 'status')
    list_filter = ('sport_type', 'status')
    search_fields = ('name', 'location', 'organizer')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registration_date')
    list_filter = ('event', 'user')
    search_fields = ('event__name', 'user__username')

# Register your models here.
