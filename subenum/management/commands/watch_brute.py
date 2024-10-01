import subprocess , os , tempfile , json
from django.core.management.base import BaseCommand
from programms.models import Programm
from subenum.models import Subdomains


def check_domain(domain):
    try:
        programs = Programm.objects.all()
        for program in programs:
            scopes = program.scopes
            if domain in scopes:
                return {'res':1 , 'program_name':program}
    except Programm.DoesNotExist:
        print("not")



def create_tmp(data , domain):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp_file:
        for value in data : 
            tmp_file.write(value[:-1]+f'.{domain}\n')
        tmp_file.flush()

    return tmp_file



def upsert_subdomain(program_name , subdomain , provider):

    exist = Subdomains.objects.filter(programm_name=program_name , subdomain=subdomain).first()
    if exist:
        if provider not in exist.providers:
            exist.providers.append(provider)
            exist.save()
            print(f'updated subdomain: {subdomain}')
    else:
        new_subdomain = Subdomains(programm_name=program_name, subdomain=subdomain, providers=[provider])
        new_subdomain.save()
        print(f'Inserted new subdomain: {subdomain}')




def run_static(domain, tmp):
    """
    Run dnsx command with the given domain/program name and return the output along with its length.
    """
    command = f"shuffledns -list {tmp} -silent -d {domain} -mode resolve -t 30 -r resolver"
    try:
        # Determine the current operating system
        if os.name == 'nt':  # Windows
            shell = r'C:\Windows\System32\cmd.exe'
        else:  # Unix-based systems
            shell = '/bin/zsh'
        
        # Execute the command in the determined shell and capture the output
        output = subprocess.check_output(command, shell=True, executable=shell)
        # Delete tmp file
        os.remove(tmp)
        # Decode the output from bytes to string
        output = output.decode('utf-8')
        output = output.strip().split('\n')
        return output
    
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print(f"Error running command: {e}")
        return None, None




class Command(BaseCommand):
    help = "Run subfinder command with the given domain"

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str, help='Domain to run subfinder on')

    def handle(self, *args, **options):
        domain = options['domain']
        if check_domain(domain)['res'] == 1:
            with open("sub.merged", "r", encoding='utf-8') as data_file:
                # You can process line by line instead of loading everything at once
                tmp_file = create_tmp(data_file, domain)
            result = run_static(domain , tmp_file.name)
            if result:
                for sub in result:
                    if sub == domain or sub == 'www.'+domain or sub == '':
                        continue
                    else:
                        upsert_subdomain(check_domain(domain)['program_name'] , sub , 'dns-brute')

