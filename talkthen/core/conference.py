import random
import string
import twilio.twiml
from twilio.rest import TwilioRestClient
from talkthen.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_CALLER_ID

def start_call(number, call_pk):
  client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

  call = client.calls.create(to=number, from_=TWILIO_CALLER_ID, \
      url='http://www.ianww.com/talkthen/core/call_placed/%s/' % call_pk)

  return call.sid

def schedule_call(from_num, to_num):
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

  # Ensure nothing outside US
  if not to_phone.number.startswith('+1') or not from_phone.number.startswith('+1'):
    return {
            'success': False,
            'message': 'We do not currently support numbers outside the US',
            }

  newcall = Call(owner_number=from_phone)
  newcall.participant_numbers.add(to_phone)
  newcall.description = 'placeholder desc'
  newcall.scheduled_for = datetime.datetime.now()
  newcall.confirmation_code = generate_confirmation_code()

  newcall.save()

  # Send confirmation text
  client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
  confirm_msg = 'Confirm your call with %s by responding with: %s' % \
          (from_phone.number, newcall.confirmation_code)
  client.messages.create(to=to_phone.number, from_=TWILIO_CALLER_ID,
          body=confirm_msg)

  return {
          'success': True,
          }

def generate_confirmation_code():
  return random_char(5).lower()

def random_char(y):
  return ''.join(random.choice(string.ascii_letters) for x in range(y))
