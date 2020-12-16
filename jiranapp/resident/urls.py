from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path(r'home', resident_home, name='resident_home'),
    path(r'visitors', visitors_resident_view, name='resident_visitors'),
    path(r'visitors/register', RegisterVisitorResidentView.as_view(), name='resident_register_visitors'),
    path(r'visitors/cancel_registration/<int:visitor_id>', cancel_visitor_resident_view, name='resident_cancel_register_visitor'),
    path(r'notice_board', NoticeBoardResidentView.as_view(), name='resident_notice_board'),
    path(r'notice_board/<int:notice_id>', notice_resident_view, name='resident_notice'),
    path(r'feedback', FeedbackResidentView.as_view(), name='resident_feedback'),
    path(r'feedback/thanks', TemplateView.as_view(template_name='resident_feedback_sent.html'), name='resident_feedback_sent'),
    path(r'facilities', facilities_resident_view, name='resident_facilities'),
    path(r'facilities/<int:facility_id>', facility_resident_view, name='resident_facility'),
    path(r'facilities/cancel_booking/<int:booking_id>', cancel_facility_booking_resident_view, name='resident_cancel_facility_booking'),
    path(r'events', events_resident_view, name='resident_events'),
    path(r'events/host', host_event_resident_view, name='resident_host_event'),
    path(r'events/manage/<int:event_id>', manage_event_resident_view, name='resident_manage_event'),
    path(r'events/manage/<int:event_id>/invite_resident', manage_event_invite_resident_view, name='resident_manage_event_invite_resident'),
    path(r'fees', fees_resident_view, name='resident_fees'),
]