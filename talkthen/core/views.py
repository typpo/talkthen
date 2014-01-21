from django.shortcuts import render, get_object_or_404

import twilio.twiml
from talkthen.core.models import Call

def call_placed(request, call_pk):
  # This handler is called when a conference is initially connected to the
  # organizer.  It determines who this person should be connected with, and
  # then connects them.

  # TODO check dialing number
  # TODO make sure this request comes from twilio

  resp = twilio.twiml.Response()
  call = get_object_or_404(Call, pk=call_pk)
  resp.dial(call.participant_numbers[0].number)   # only support 2-person calls for now

  return str(resp)
