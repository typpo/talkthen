import datetime
import random
import string

import twilio.twiml
from twilio.rest import TwilioRestClient
from talkthen.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_CALLER_ID

from core.models import Call, PhoneNumber

def start_call(number, call_pk):
  client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

  call = client.calls.create(to=number, from_=TWILIO_CALLER_ID, \
      url='http://www.ianww.com/talkthen/core/call_placed/%s/' % call_pk)

  return call.sid

def schedule_call(from_num, to_num):
  from_num = PhoneNumber.convert_to_e164(from_num)
  to_num = PhoneNumber.convert_to_e164(to_num)
  try:
    from_phone = PhoneNumber.objects.get(number=from_num)
  except PhoneNumber.DoesNotExist:
    from_phone = PhoneNumber(number=from_num)
    from_phone.save()

  try:
    to_phone = PhoneNumber.objects.get(number=to_num)
  except PhoneNumber.DoesNotExist:
    to_phone = PhoneNumber(number=to_num)
    to_phone.save()

  # Ensure nothing outside US
  if not to_phone.number.startswith('+1') or not from_phone.number.startswith('+1'):
    return {
            'success': False,
            'message': 'We do not currently support numbers outside the US',
            }

  newcall = Call()
  newcall.owner_number = from_phone
  newcall.description = 'placeholder desc'
  newcall.scheduled_for = datetime.datetime.now()
  newcall.remind_at = datetime.datetime.now()
  newcall.confirmation_code = generate_confirmation_code()

  newcall.save()
  newcall.participant_numbers.add(to_phone)
  newcall.save()

  # Send confirmation text
  client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
  # TODO change to numbers
  confirm_msg = 'Confirm your call with %s by responding with: %s (not case sensitive)' % \
          (from_phone.number, newcall.confirmation_code)
  client.messages.create(to=from_phone.number, from_=TWILIO_CALLER_ID,
          body=confirm_msg)

  return {
          'success': True,
          }

def generate_confirmation_code():
  return random_code(5).lower()

def random_code(y):
  return ''.join(str(random.randint(0, 9)) for x in range(y))
