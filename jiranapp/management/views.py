from django.shortcuts import render
from rest_framework import generics
from jiranapp.serializers import *


# Create your views here.
class ResidentListManagementView(generics.ListCreateAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer


class HouseholdListManagementView(generics.ListCreateAPIView):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer


class NoticeManagementView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer


class FeedbackManagementView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FacilitiesListManagementView(generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
