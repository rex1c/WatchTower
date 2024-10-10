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
            os.system(f'python3 manage.py watch_crtsh {scope}')
            os.system(f'python3 manage.py watch_subfinder {scope}')
            os.system(f'python3 manage.py watch_abuseipdb {scope}')
            os.system(f'python3 manage.py watch_certify {scope}')
            os.system(f'python3 manage.py watch_chaos {scope}')
            os.system(f'python3 manage.py watch_waysub {scope}')
    time_threshold = timezone.now() - timedelta(hours=12)
    livesubdomains = LiveSubdomains.objects.all().filter(last_update__gte=time_threshold)
    if livesubdomains:
        for subdomain in livesubdomains:
            print(f'subdomain : {subdomain.subdomain}')
            os.system(f'python3 manage.py watch_certify {subdomain.subdomain}')
class Command(BaseCommand):
    def handle(self, *args, **options):
        run_all()
        
