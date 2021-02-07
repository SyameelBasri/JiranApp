from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

USER_TYPES = (
    ('RESIDENT', 'RESIDENT'),
    ('MANAGEMENT', 'MANAGEMENT'),
    ('SECURITY', 'SECURITY')
)

NOTIFICATION_TIER = (
    ('CRITICAL', 'CRITICAL'),
    ('NORMAL', 'NORMAL'),
    ('LOW', 'LOW')
)

FEEDBACK_CATEGORY = (
    ('PROBLEM', 'PROBLEM'),
    ('SUGGESTION', 'SUGGESTION'),
    ('OTHER', 'OTHER')
)


# Create your models here.
class Account(AbstractUser):
    name = models.CharField("Name of Account", "Name", max_length=64)
    ic = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    user_type = models.CharField("User Type", max_length=10, choices=USER_TYPES)
    created_at = models.DateTimeField("Created At", auto_now_add=True)


class Household(models.Model):
    address = models.CharField(max_length=255)


class Resident(models.Model):
    id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    household = models.ForeignKey(Household, related_name='belongs_to', on_delete=models.CASCADE)


class Visitor(models.Model):
    name = models.CharField("Visitor Name", max_length=64)
    ic = models.CharField("Visitor IC No.", max_length=20)
    phone = models.CharField("Visitor Contact", max_length=12)
    date = models.DateField('Visiting Date')
    start_time = models.TimeField()
    end_time = models.TimeField()
    invited_by = models.ForeignKey(Household, related_name='registered_by', on_delete=None)


class Notice(models.Model):
    tier = models.CharField(max_length=20, choices=NOTIFICATION_TIER)
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(Account, related_name='posted_by_management', on_delete=None)


class Feedback(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=FEEDBACK_CATEGORY)
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(Account, related_name='posted_by_resident', on_delete=None)


class Event(models.Model):
    host = models.ForeignKey(Resident, related_name='hoseted_by_resident', on_delete=models.CASCADE)
    name = models.CharField("Event Name", max_length=64)
    description = models.TextField(blank=True, null=True)
    address = models.CharField("Venue", max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    invitees = models.ManyToManyField('Account', through='EventInvitation')


class EventInvitation(models.Model):
    event = models.ForeignKey(Event, related_name='invited_to', on_delete=models.CASCADE)
    visitor = models.OneToOneField(Visitor, related_name='visitor_invited_to', on_delete=models.CASCADE, blank=True, null=True)
    resident = models.ForeignKey(Account, related_name='resident_invited_to', on_delete=models.CASCADE, blank=True, null=True)
    is_attending = models.BooleanField(default=False)
    has_responded = models.BooleanField(default=False)

    class Meta:
        unique_together = (('event', 'resident'))


class Facility(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    is_open = models.BooleanField(default=True)
    img_url = models.CharField(max_length=255)


class FacilityBooking(models.Model):
    facility = models.ForeignKey(Facility, related_name='booking_for_facility', on_delete=models.CASCADE)
    event = models.OneToOneField(Event, related_name='booking_for_event', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField('Booking date')
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked_by = models.ForeignKey(Account, related_name='booking_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField("Created At", auto_now_add=True)


class FeesCharged(models.Model):
    household = models.ForeignKey(Household, related_name='charged_to_household', on_delete=None)
    amount = models.FloatField()
    description = models.CharField(max_length=64)
    date_charged = models.DateField()
    due_date = models.DateField()


class Payment(models.Model):
    household = models.ForeignKey(Household, related_name='payed_for_household', on_delete=None)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
