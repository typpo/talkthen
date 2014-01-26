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

def create(request, from_num, to_num):

  resp = conference.schedule_call(from_num, to_num)
  return HttpResponse(json.dumps(resp))


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
def text_confirmation_reply(request):
  from_number = request.REQUEST.get('From', None)
  msg = request.REQUEST.get('Body', None)

  print 'Got MSG from %s: %s' % (from_number, msg)

  # TODO
  resp = twilio.twiml.Response()
  resp.message(message)

  return HttpResponse(str(resp))


def associate_email():
  # Record email under a phone number
  pass
