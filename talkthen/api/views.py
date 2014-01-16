from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from core.models import PhoneNumber, Call

class PhoneNumberViewSet(viewsets.ModelViewSet):
  model = PhoneNumber

class CallViewSet(viewsets.ModelViewSet):
  model = Call
