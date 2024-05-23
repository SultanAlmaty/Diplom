from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventRegistration
from .forms import EventRegistrationForm
from django.utils.dateparse import parse_date

# Create your views here.

def index(request):
    return render(request, 'gornyak/index.html')

@login_required
def register_for_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.error(request, 'You have already registered for this event.')
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.save()
            messages.success(request, 'You have successfully registered for the event.')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventRegistrationForm(initial={'event': event, 'user': request.user})

    return render(request, 'gornyak/register_for_event.html', {'form': form, 'event': event})


def event_list(request):
    sport_type = request.GET.get('sport_type')
    location = request.GET.get('location')
    date = request.GET.get('date')

    events = Event.objects.all()

    if sport_type:
        events = events.filter(sport_type=sport_type)
    if location:
        events = events.filter(location=location)
    if date:
        events = events.filter(start_datetime__date__gte=parse_date(date))

    # Получение уникальных значений для типов спорта и локаций
    sport_types = Event.objects.values_list('sport_type', flat=True).distinct()
    locations = Event.objects.values_list('location', flat=True).distinct()

    return render(request, 'gornyak/event_list.html', {
        'events': events,
        'sport_types': sport_types,
        'locations': locations,
    })

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'gornyak/event_detail.html', {'event': event})