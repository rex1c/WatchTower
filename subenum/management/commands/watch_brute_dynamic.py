import subprocess , os , tempfile , tldextract
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from programms.models import Programm
from ns.models import LiveSubdomains
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



def get_domain_tld(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"



def create_tmp(data):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp_file:
        for value in data : 
            tmp_file.write(value+'\n')
        tmp_file.flush()

    return tmp_file



def upsert_subdomain(program_name , subdomain , provider):
    try:
        programs = Programm.objects.all().filter(programm_name=program_name)
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





def run_dynamic(domain, tmp):
    """
    Run dynamic brute command with the given domain/program name and return the output along with its length.
    """
    os.system(f'cat {tmp} | dnsgen -w ./tmp/words.merged - | sort -u >> ./tmp/dnsgen.txt')
    os.system(f'altdns -i {tmp} -w ./tmp/words.merged -o ./tmp/altdns.txt')
    os.system('cat ./tmp/altdns.txt ./tmp/dnsgen.txt | sort -u >> ./tmp/combined.txt')
    # Delete tmp file
    os.remove(tmp)
    command = f"shuffledns -list ./tmp/combined.txt -silent -d {domain} -mode resolve -t 500 -r ./tmp/resolver"
    try:
        # Determine the current operating system
        if os.name == 'nt':  # Windows
            shell = r'C:\Windows\System32\cmd.exe'
        else:  # Unix-based systems
            shell = '/bin/zsh'
        
        # Execute the command in the determined shell and capture the output
        output = subprocess.check_output(command, shell=True, executable=shell)
        # Delete tmp files
        os.system("rm ./tmp/*.txt")
        # Decode the output from bytes to string
        output = output.decode('utf-8')
        output = output.strip().split('\n')
        return output
    
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print(f"Error running command: {e}")
        return None, None




class Command(BaseCommand):
    help = "Run dynamic brute  command with the given domain"

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str, help='Domain to run dynamic brute on')

    def handle(self, *args, **options):
        domain = options['domain']
        time_threshold = timezone.now() - timedelta(hours=12)
        livesubdomains = LiveSubdomains.objects.all().filter(subdomain__endswith=f'.{domain}', last_update__gte=time_threshold).values()
        lives = [subdomain['subdomain'] for subdomain in livesubdomains]
        result = run_dynamic(domain , create_tmp(lives).name)
        if result:
            for sub in result:
                if sub == domain or sub == 'www.'+domain or sub == '':
                    continue
                else:
                    upsert_subdomain(check_domain(domain)['program_name'] , sub , 'dynamic-brute')
