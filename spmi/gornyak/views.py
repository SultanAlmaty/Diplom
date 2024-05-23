from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Event, EventRegistration, Sport, Location
from .forms import EventRegistrationForm
from django.utils.dateparse import parse_date

# Create your views here.

def index(request):
    return render(request, 'gornyak/index.html')

def event_list(request):
    events = Event.objects.all()
    sport_types = Sport.objects.all()
    locations = Location.objects.all()

    selected_sport = request.GET.get('sport_type')
    selected_location = request.GET.get('location')
    selected_date = request.GET.get('date')

    if selected_sport:
        events = events.filter(sport_type__id=selected_sport)
    if selected_location:
        events = events.filter(location__id=selected_location)
    if selected_date:
        events = events.filter(start_datetime__date__gte=selected_date)

    return render(request, 'gornyak/event_list.html', {
        'events': events,
        'sport_types': sport_types,
        'locations': locations,
        'selected_sport': selected_sport,
        'selected_location': selected_location,
        'selected_date': selected_date,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_registered = False
    if request.user.is_authenticated:
        user_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
    registration_count = EventRegistration.objects.filter(event=event).count()
    return render(request, 'gornyak/event_detail.html', {
        'event': event,
        'user_registered': user_registered,
        'registration_count': registration_count,
    })

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not EventRegistration.objects.filter(event=event, user=request.user).exists():
        EventRegistration.objects.create(event=event, user=request.user)
    return redirect(reverse('event_detail', args=[event.id]))