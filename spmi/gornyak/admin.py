from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
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
