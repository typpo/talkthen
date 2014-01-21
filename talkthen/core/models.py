from django.db import models

class PhoneNumber(models.Model):
  number = models.CharField(max_length=50, unique=True)
  name = models.CharField(max_length=50, blank=True)
  email = models.EmailField(max_length=128, blank=True)

class Call(models.Model):
  owner_number = models.ForeignKey(PhoneNumber)
  participant_numbers = models.ManyToManyField(PhoneNumber, related_name='call_participants')

  description = models.CharField(max_length=300, blank=True)
  scheduled_for = models.DateTimeField()

  called = models.BooleanField(default=False)

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
