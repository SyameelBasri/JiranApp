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
        fields = ('title', 'category', 'content')


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
        exclude = {'host', 'created_at', 'invitees'}
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'start_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.widgets.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


class EventInviteVisitorForm(ModelForm):
    class Meta:
        model = Visitor
        exclude = ('invited_by', 'date', 'start_time', 'end_time')


class EventInviteResidentForm(ModelForm):
    class Meta:
        model = Event
        fields = ('invitees',)
        widgets = {
            'invitees': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        event = kwargs['instance']
        super(EventInviteResidentForm, self).__init__(*args, **kwargs)
        id_to_exclude = [ o.resident.id for o in EventInvitation.objects.filter(event=event.id) ]
        id_to_exclude.append(user.id)
        self.fields['invitees'].queryset = Account.objects.exclude(id__in=id_to_exclude)
