import datetime
import time

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import twilio.twiml
from core.models import Call, PhoneNumber

def create(request, from_num, to_num):
  # TODO ensure nothing outside of the US

  # Convert to standard number format
  from_num = PhoneNumber.convert_to_e164(from_num)
  to_num = PhoneNumber.convert_to_e164(to_num)

  # Create a call from
  try:
    from_phone = Phone.objects.get(number=from_num)
  except:
    from_phone = Phone(number=from_num)
    from_phone.save()

  try:
    to_phone = Phone.objects.get(number=to_num)
  except:
    to_phone = Phone(number=to_num)
    to_phone.save()

  newcall = Call(owner_number=from_phone)
  newcall.participant_numbers.add(to_phone)
  newcall.description = 'placeholder desc'
  newcall.scheduled_for = datetime.datetime.now()

  newcall.save()

  return ''


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def call_placed(request, call_pk):
  # This handler is called when a conference is initially connected to the
  # organizer.  It determines who this person should be connected with, and
  # then connects them.

  # TODO check dialing number
  # TODO make sure this request comes from twilio

  resp = twilio.twiml.Response()
  call = get_object_or_404(Call, pk=call_pk)
  resp.say('Hello. You are being connected.')
  # Only supporting 2-person calls for now
  # TODO Time limit would go here
  # TODO pass action to handle call status
  # TODO conference stuff https://www.twilio.com/docs/api/twiml/conference
  # TODO record call length
  resp.dial(call.participant_numbers.all()[0].number,
      callerId=call.owner_number.number)
  resp.say('The call has ended.  You may hang up now.')

  return HttpResponse(str(resp))
