from django.db import models
import phonenumbers

class PhoneNumber(models.Model):
  number = models.CharField(max_length=50, unique=True)
  name = models.CharField(max_length=50, blank=True)
  email = models.EmailField(max_length=128, blank=True)

  def convert_to_e164(raw_phone):
    if not raw_phone:
      return

    if raw_phone[0] == '+':
      # Phone number may already be in E.164 format.
      parse_type = None
    else:
      # If no country code information present, assume it's a US number
      parse_type = "US"

    phone_representation = phonenumbers.parse(raw_phone, parse_type)
    return phonenumbers.format_number(phone_representation,
      phonenumbers.PhoneNumberFormat.E164)

class Call(models.Model):
  owner_number = models.ForeignKey(PhoneNumber)
  participant_numbers = models.ManyToManyField(PhoneNumber, related_name='call_participants')

  description = models.CharField(max_length=300, blank=True)
  scheduled_for = models.DateTimeField()

  called = models.BooleanField(default=False)
  canceled = models.BooleanField(default=False)
  confirmed = models.BooleanField(default=False)

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
