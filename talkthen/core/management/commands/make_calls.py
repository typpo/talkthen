from django.core.management.base import NoArgsCommand

from core import conference
from core.models import Call, PhoneNumber

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for call in Call.objects.all():
            print 'Handling %s...' % call
            conference.start_call(call.owner_number.number, call.pk)
