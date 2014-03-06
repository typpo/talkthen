import datetime
import time
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import send_mail

import twilio.twiml
from core.models import Call, PhoneNumber

import conference

@require_http_methods(['POST'])
@csrf_exempt     # TODO should not be
def create_call(request):
  from_num = request.POST['from']
  to_num = request.POST['to']
  # Convert from UNIX timestamp in milliseconds to timestamp in seconds
  when = datetime.datetime.utcfromtimestamp(int(request.POST['when']))
  strfwhen = when.strftime('%Y-%m-%d %H:%M:%S')
  email = request.POST.get('email', None)
  print 'scheduling call %s to %s @ %s w/ email %s' % \
      (from_num, to_num, strfwhen, email)
  if from_num and to_num:
    resp = conference.schedule_call(from_num, to_num, when, email)
    if resp['success'] and email:
      # Send confirmation email
      email_msg = """Hello,

This email confirms a call scheduled for %s <a href="http://www.worldtimebuddy.com/?pl=1&lid=100,5,8&h=8">UTC</a>.  You will be dialed at %s and connected with %s.

Be sure to reply to the text message on your phone with the confirmation code.  Otherwise, the call will not be placed.

- talkThen bot
      """ % (strfwhen, from_num, to_num)
      send_mail('Your call has been scheduled', email_msg, 'talkThen@talkthen.com', [email])
    return HttpResponse(json.dumps(resp))
  return HttpResponse("{'success': False, 'message': 'Invalid request'}")


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
  resp.say('Hello. You are being connected by TalkThen.')
  # Only supporting 2-person calls for now
  # TODO Time limit would go here
  # TODO pass action to handle call status
  # TODO conference stuff https://www.twilio.com/docs/api/twiml/conference
  resp.dial(call.participant_numbers.all()[0].number,
      callerId=call.owner_number.number)
  resp.say('The call has ended.  You may hang up now.')

  # Mark call as done!
  call.called = True
  call.save()

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
