from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventRegistration
from .forms import EventRegistrationForm

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
    events = Event.objects.all()
    return render(request, 'gornyak/event_list.html', {'events': events})