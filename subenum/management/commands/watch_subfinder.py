import subprocess , os , tldextract 
from django.core.management.base import BaseCommand
from programms.models import Programm  
from subenum.models import Subdomains


def get_domain_tld(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"



def check_domain(domain):
    try:
        programs = Programm.objects.all()
        for program in programs:
            scopes = program.scopes
            if domain in scopes:
                return {'res':1 , 'program_name':program}
    except Programm.DoesNotExist:
        print("not")



def upsert_subdomain(program_name , subdomain , provider):
    try:
        programs = Programm.objects.all()
        for program in programs:
            scopes = program.scopes
            ooscopes = program.ooscopes
            if get_domain_tld(subdomain) not in scopes or subdomain in ooscopes:
                print(f"subdomain is not in scope: {subdomain}")
                return True

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

    except Programm.DoesNotExist:
        print("not")



def run_subfinder(domain):
    """
    Run subfinder command with the given domain and return the output along with its length.
    """
    command = f"subfinder -d {domain} -all"
    try:
        # Determine the current operating system
        if os.name == 'nt':  # Windows
            shell = r'C:\Windows\System32\cmd.exe'
        else:  # Unix-based systems
            shell = '/bin/zsh'
        
        # Execute the command in the determined shell and capture the output
        output = subprocess.check_output(command, shell=True, executable=shell)
        # Decode the output from bytes to string
        output = output.decode('utf-8')
        # Calculate the length of the output
        output_length = len(output.splitlines())
        return output.splitlines(), output_length
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
            result, result_length = run_subfinder(domain)
            if result:
                for sub in result:
                    sub = sub.replace('*.', '')
                    if sub == domain or sub == 'www.'+domain or sub == get_domain_tld(domain):
                        continue
                    else:
                        upsert_subdomain(check_domain(domain)['program_name'] , sub , 'subfinder')
        else:
            pass