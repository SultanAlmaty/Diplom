from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from accounts.forms import LoginUserForm
from gornyak.models import EventRegistration, Event, Sport, Location


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('event_list')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))

@login_required
def profile(request):
    sport_type = request.GET.get('sport_type')
    location = request.GET.get('location')
    date = request.GET.get('date')
    event_type = request.GET.get('event_type')
    status = request.GET.get('status')

    registrations = EventRegistration.objects.filter(user=request.user)

    events = Event.objects.filter(id__in=registrations.values('event_id'))

    if sport_type:
        events = events.filter(sport_type__id=sport_type)
    if location:
        events = events.filter(location__id=location)
    if date:
        events = events.filter(start_datetime__date=date)
    if event_type:
        events = events.filter(event_type=event_type)
    if status:
        events = events.filter(status=status)

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

    return render(request, 'accounts/profile.html', context)