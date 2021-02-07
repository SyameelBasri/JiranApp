from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, render_to_response, redirect
from django.views import View
from rest_framework import generics
from jiranapp.serializers import *
from jiranapp.models import *

from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .forms import *


# Create your views here.
def resident_home(request):
    notices = Notice.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'notices':notices})


def visitors_resident_view(request):
    visitors = Visitor.objects.filter(invited_by=Resident.objects.get(id=request.user).household).order_by('date', 'start_time')

    return render(request, 'resident_visitors.html', {'visitors':visitors})


class RegisterVisitorResidentView(FormView):
    template_name = 'resident_visitors_invite.html'
    form_class = VisitorInviteForm
    user = None

    def form_valid(self, form):
        self.get_context_data()
        self.object = form.save(commit=False)
        self.object.invited_by = Resident.objects.get(id=self.user).household
        self.object.save()
        return redirect('resident_visitors')

    def get_context_data(self, **kwargs):
        c = super(RegisterVisitorResidentView, self).get_context_data(**kwargs)
        self.user = self.request.user
        return c


class EditVisitorResidentView(UpdateView):
    model = Visitor
    template_name = 'resident_visitors_edit.html'
    form_class = VisitorInviteForm
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('resident_visitors')


def cancel_visitor_resident_view(request, visitor_id):
    try:
        Visitor.objects.get(id=visitor_id).delete()
    except Visitor.DoesNotExist:
        pass
    return redirect('resident_visitors')


class NoticeBoardResidentView(ListView):
    template_name = 'resident_notice_board.html'
    model = Notice
    ordering = ['-date']


def notice_resident_view(request, notice_id):
    try:
        notice = Notice.objects.get(id=notice_id)
    except Notice.DoesNotExist:
        notice = None
    return render(request, 'resident_notice.html', {'notice': notice})


class FeedbackResidentView(FormView):
    template_name = 'resident_feedback.html'
    form_class = FeedbackForm
    success_url = 'feedback/thanks'
    user = None

    def form_valid(self, form):
        self.get_context_data()
        self.object = form.save(commit=False)
        self.object.posted_by = self.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        c = super(FeedbackResidentView, self).get_context_data(**kwargs)
        self.user = self.request.user
        return c


def facilities_resident_view(request):
    facilities = Facility.objects.all()
    bookings = FacilityBooking.objects.filter(booked_by=request.user).order_by('-date', '-start_time')

    return render(request, 'resident_facilities.html', {'facilities': facilities, 'bookings':bookings})


def facility_resident_view(request, facility_id):
    try:
        facility = Facility.objects.get(id=facility_id)
        form = FacilityBookingForm(request.POST)

        if form.is_valid():
            object = form.save(commit=False)
            object.facility = facility
            object.booked_by = request.user
            object.save()
            return redirect('resident_facilities')

    except Facility.DoesNotExist:
        facility = None
        form = None
    return render(request, 'resident_facility.html', {'facility': facility, 'form':form})


def cancel_facility_booking_resident_view(request, booking_id):
    try:
        FacilityBooking.objects.get(id=booking_id).delete()
    except FacilityBooking.DoesNotExist:
        pass
    return redirect('resident_facilities')


def events_resident_view(request):
    pending_invitations = EventInvitation.objects.filter(resident=request.user, has_responded=False)
    events_attending = EventInvitation.objects.filter(resident=request.user, is_attending=True)
    events_hosting = Event.objects.filter(host=Resident.objects.get(id=request.user))

    return render(request, 'resident_events.html', {'pending_invitations':pending_invitations,
                                                    'events_attending':events_attending,
                                                    'events_hosting':events_hosting,})


def host_event_resident_view(request):
    form = EventHostForm(request.POST)

    if form.is_valid():
        object = form.save(commit=False)
        object.host = Resident.objects.get(id=request.user)
        object.save()
        return redirect('resident_events')

    return render(request, 'resident_host_event.html', {'form':form})


def manage_event_resident_view(request, event_id):
    event = Event.objects.get(id=event_id)
    invitees = EventInvitation.objects.filter(event=event)
    attendees = EventInvitation.objects.filter(event=event, is_attending=True)

    return render(request, 'resident_manage_event.html', {'event':event, 'invitees':invitees, 'attendees':attendees})


class EventInviteResidentView(UpdateView):
    model = Event
    template_name = 'manage_event_invite_resident.html'
    form_class = EventInviteResidentForm

    def form_valid(self, form):
        form.save(commit=True)
        return redirect('resident_events')
    
    def get_form_kwargs(self):
        kwargs = super(EventInviteResidentView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


def fees_resident_view(request):
    household = Resident.objects.get(id=request.user).household
    fees_charged = FeesCharged.objects.filter(household=household)
    payments = Payment.objects.filter(household=household)

    charged_amount = fees_charged.aggregate(Sum('amount'))
    paid_amount = payments.aggregate(Sum('amount'))

    if charged_amount['amount__sum'] is None:
        charged_amount['amount__sum'] = 0

    if paid_amount['amount__sum'] is None:
        paid_amount['amount__sum'] = 0

    net = charged_amount['amount__sum']-paid_amount['amount__sum']

    return render(request, 'resident_fees.html', {'fees_charged':fees_charged, 'payments':payments, 'charged_amount':charged_amount, 'paid_amount':paid_amount, 'net':net})



