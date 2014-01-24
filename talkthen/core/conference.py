import twilio.twiml
from twilio.rest import TwilioRestClient
from talkthen.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_CALLER_ID

def start_call(number, call_pk):
  client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

  call = client.calls.create(to=number, from_=TWILIO_CALLER_ID, \
      url='http://www.ianww.com/talkthen/core/call_placed/%s/' % call_pk)

  return call.sid
