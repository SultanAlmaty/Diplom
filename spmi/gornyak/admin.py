from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
from .models import Event, EventRegistration, Sport, Location


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_datetime', 'end_datetime', 'location', 'sport_type', 'status', 'registration_open', 'event_type')
    list_editable = ('registration_open',)
    list_filter = ('sport_type', 'status', 'event_type')
    search_fields = ('name', 'location', 'organizer')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registration_date')
    list_filter = ('event', 'user')
    search_fields = ('event__name', 'user__username')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('middle_name', 'group_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'middle_name', 'group_name', 'password1', 'password2')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
