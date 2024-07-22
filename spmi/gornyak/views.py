from django.core.paginator import Paginator
from django.db.models import Case, When, Value, IntegerField
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Event, EventRegistration, Sport, Location
from .forms import EventRegistrationForm
from django.utils.dateparse import parse_date


def index(request):
    return render(request, 'gornyak/base.html')

def event_list(request):
    sport_type = request.GET.get('sport_type')
    location = request.GET.get('location')
    date = request.GET.get('date')
    event_type = request.GET.get('event_type')
    status = request.GET.get('status')

    events = Event.objects.all()

    if sport_type:
        events = events.filter(sport_type__id=sport_type)
    if location:
        events = events.filter(location__id=location)
    if date:
        events = events.filter(start_datetime__date__gte=date)
    if event_type:
        events = events.filter(event_type=event_type)
    if status:
        events = events.filter(status=status)

    events = events.annotate(
        status_order=Case(
            When(status='registration', then=Value(1)),
            When(status='completed', then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
    ).order_by('status_order', 'start_datetime')

    paginator = Paginator(events, 10)  # 10 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sport_types': Sport.objects.all(),
        'locations': Location.objects.all(),
        'selected_sport': sport_type,
        'selected_location': location,
        'date': date,
        'selected_event_type': event_type,
        'selected_status': status,
        'page_obj': page_obj,
    }
    return render(request, 'gornyak/event_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_registered = False
    if request.user.is_authenticated:
        user_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
        registration_count = EventRegistration.objects.filter(event=event).count()
        if request.method == 'POST':
            if not user_registered and event.registration_open:
                EventRegistration.objects.create(event=event, user=request.user)
                return redirect('event_detail', event_id=event.id)
    else:
        return redirect('accounts:login')


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