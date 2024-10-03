import os 
from django.core.management.base import BaseCommand
from programms.models import Programm 


def run_all():
    programms = Programm.objects.all()
    for programm in programms:
        print(f'program name : {programm.programm_name}')
        os.system(f'python3 manage.py watch_httpx {programm.programm_name}')

class Command(BaseCommand):
    def handle(self, *args, **options):
        run_all()
        
