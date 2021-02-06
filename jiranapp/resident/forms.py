from django import forms
from django.forms import ModelForm, Form, fields
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from jiranapp.models import *


class ResidentAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Username or email address or phone number',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('category', 'content')


class FacilityBookingForm(ModelForm):
    class Meta:
        model = FacilityBooking
        fields = ('date', 'start_time', 'end_time')
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'start_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


class VisitorInviteForm(ModelForm):
    class Meta:
        model = Visitor
        exclude = ('invited_by',)
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'start_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


class EventHostForm(ModelForm):
    class Meta:
        model = Event
        exclude = {'host', 'created_at'}
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'start_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


class EventInviteVisitorForm(ModelForm):
    class Meta:
        model = Visitor
        exclude = ('invited_by', 'date', 'start_time', 'end_time')


class EventInviteResidentForm(Form):
    invited_residents = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Account.objects.all(), to_field_name='Name')