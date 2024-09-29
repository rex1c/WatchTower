import os 
from django.core.management.base import BaseCommand
from programms.models import Programm 


def run_all():
    programms = Programm.objects.all()
    for programm in programms:
        print(f'program name : {programm.programm_name}')
        scopes = programm.scopes
        for scope in scopes:
            os.system(f'python3 manage.py watch_crtsh {scope}')
            os.system(f'python3 manage.py watch_subfinder {scope}')
            os.system(f'python3 manage.py watch_abuseipdb {scope}')

class Command(BaseCommand):
    def handle(self, *args, **options):
        run_all()
        
