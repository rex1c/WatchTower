import os
import json
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand
from programms.models import Programm  # replace 'yourapp' with the actual name of your Django app

class Command(BaseCommand):
    help = 'Import JSON files into database'

    def handle(self, *args, **options):
        # Get all JSON files in the directory
        json_files = [f for f in os.listdir('.') if f.endswith('.json')]

        for file in json_files:
            with open(file, 'r') as f:
                data = json.load(f)

                # Check if a Programm instance with the same programm_name already exists
                programm_name = data.get('programm_name', file.replace('.json', ''))
                try:
                    programm = Programm.objects.get(programm_name=programm_name)
                    self.stdout.write(self.style.WARNING(f'Checking existing programm: {programm_name}'))
                except Programm.DoesNotExist:
                    programm = Programm()
                    programm.programm_name = programm_name
                    self.stdout.write(self.style.SUCCESS(f'Creating new programm: {programm_name}'))

                # Check if fields have changed
                if programm.config == data.get('config', {}) and \
                   programm.scopes == data.get('scopes', {}) and \
                   programm.ooscopes == data.get('ooscopes', {}):
                    self.stdout.write(self.style.SUCCESS(f'No changes detected in {file}. Skipping update.'))
                    continue

                # Update the instance's fields
                programm.config = data.get('config', {})
                programm.scopes = data.get('scopes', {})
                programm.ooscopes = data.get('ooscopes', {})

                # Save the instance to the database
                programm.save()

                self.stdout.write(self.style.SUCCESS(f'Imported {file}'))