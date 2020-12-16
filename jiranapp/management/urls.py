from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path(r'residents', ResidentListManagementView.as_view(), name='management_residents_list'),
    path(r'households', HouseholdListManagementView.as_view(), name='management_households_list'),
    path(r'notice_board', NoticeManagementView.as_view(), name='management_notice_board'),
    path(r'feedback', FeedbackManagementView.as_view(), name='management_feedback'),
    path(r'facilities', FacilitiesListManagementView.as_view(), name='management_facilities')
]