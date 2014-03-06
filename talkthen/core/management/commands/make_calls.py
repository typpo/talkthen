import datetime
import pytz

from django.core.management.base import NoArgsCommand

from core import conference
from core.models import Call, PhoneNumber

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for call in Call.objects.filter(confirmed=True, called=False):
            if (call.scheduled_for - datetime.datetime.now(pytz.utc)).total_seconds() < 60:
                print 'Handling %s...' % call
                conference.start_call(call.owner_number.number, call.pk)
            elif (call.remind_at - datetime.datetime.now(pytz.utc)).total_seconds() < 60:
                print 'Reminding %s...' % call
                conference.remind_call(call)
