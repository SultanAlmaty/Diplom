from django import forms
from .models import EventRegistration, Event

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['event', 'user']

# class EventFilterForm(forms.Form):
#     sport_type = forms.ChoiceField(
#         choices=[('', 'All')] + Event.SPORT_CHOICES,
#         required=False,
#         label='Sport Type'
#     )
#     location = forms.CharField(required=False, label='Location')
#     start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Start Date')
#     end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='End Date')