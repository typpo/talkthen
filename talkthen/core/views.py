from django.shortcuts import render, get_object_or_404

import twilio.twiml
from talkthen.core.models import Call

def call_placed(request, call_pk):
  # TODO check dialing number, check to make sure this comes from twilio
  resp = twilio.twiml.Response()
  call = get_object_or_404(Call, pk=call_pk)
  resp.dial(call.participant_numbers[0])   # only support 2-person calls for now

  return str(resp)
