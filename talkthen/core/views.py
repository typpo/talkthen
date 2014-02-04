import datetime
import time
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import twilio.twiml
from core.models import Call, PhoneNumber

import conference

@require_http_methods(['POST'])
@csrf_exempt     # TODO should not be
def create_call(request):
  from_num = request.POST['from']
  to_num = request.POST['to']
  print 'scheduling call %s to %s' % (from_num, to_num)
  if from_num and to_num:
    resp = conference.schedule_call(from_num, to_num)
    return HttpResponse(json.dumps(resp))
  return {'success': False, 'message': 'Invalid request'}


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

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def sms_received(request):
  from_number = PhoneNumber.convert_to_e164(request.REQUEST.get('From', None))
  msg = request.REQUEST.get('Body', None).strip()

  # TODO handle cancellation
  print 'Got MSG from %s: %s' % (from_number, msg)

  parts = msg.split(' ')
  if len(parts) > 1 and parts[0].lower() == 'cancel':
    code = parts[1]
    cancel = True
  else:
    code = msg
    cancel = False

  resp = twilio.twiml.Response()
  try:
    call = Call.objects.get(owner_number__number=from_number, confirmation_code=code)
  except:
    resp.message('Sorry, could not confirm your call. (1)')
    return HttpResponse(str(resp))

  if cancel:
    call.delete()
    resp.message('Your call has been cancelled.')
  else:
    call.confirmed = True
    call.save()
    resp.message('Your call is confirmed. Text "cancel %s" to cancel.' % code)
  return HttpResponse(str(resp))


def associate_email():
  # Record email under a phone number
  pass
