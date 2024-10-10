import os 
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from programms.models import Programm 
from ns.models import LiveSubdomains

def run_all():
    programms = Programm.objects.all()
    for programm in programms:
        print(f'program name : {programm.programm_name}')
        scopes = programm.scopes
        for scope in scopes:
            os.system(f'python3 manage.py watch_brute_static {scope}') # not sure to run in here
    time_threshold = timezone.now() - timedelta(hours=12)
    livesubdomains = LiveSubdomains.objects.all().filter(last_update__gte=time_threshold)
    if livesubdomains:
        for programm in programms:
            scopes = programm.scopes
            for scope in scopes:
                os.system(f'python3 manage.py watch_brute_dynamic {scope}')

class Command(BaseCommand):
    def handle(self, *args, **options):
        run_all()
        
