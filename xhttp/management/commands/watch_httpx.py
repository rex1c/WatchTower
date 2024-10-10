import subprocess , os , tldextract , json , asyncio
from django.core.management.base import BaseCommand
from telegram import Bot
from programms.models import Programm  
from ns.models import LiveSubdomains
from xhttp.models import HTTPx


TOKEN = '8192757664:AAGGVVFMczQD8r-He6lxByuscsmhc2GVq58'
CHANNEL_ID = '-1002299317030'



async def Sendmessage(message):
    bot = Bot(token=TOKEN)

    # Send a message
    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='MarkdownV2')



def get_domain_tld(url):
    extracted = tldextract.extract(url)
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"
    else:
        return False



def check_cdn(domain):
    livesudomain = LiveSubdomains.objects.all().filter(subdomain=domain).values()
    if livesudomain["cdn"]:
        return True
    else:
        return False



def check_domain(domain):
    try:
        programs = Programm.objects.all()
        for program in programs:
            scopes = program.scopes
            if domain in scopes:
                return {'res':1 , 'program_name':program}
    except Programm.DoesNotExist:
        print("not")



def upsert_httpx(program_name, subdomain, obj):
    try:
        programs = Programm.objects.all().filter(programm_name=program_name)
        for program in programs:
            scopes = program.scopes
            ooscopes = program.ooscopes
            if get_domain_tld(subdomain) not in scopes or subdomain in ooscopes:
                print(f"subdomain is not in scope: {subdomain}")
                return True

            exist = HTTPx.objects.filter(programm_name=program_name , subdomain=subdomain , url=obj.get('url')).first()
            if exist:
                if obj.get('tech',[]) != exist.tech:
                    asyncio.run((Sendmessage(f"Asset Technology changed: `{obj.get('url')}` to {obj.get('tech')} \nProgram Name: \#{program_name}")))
                if obj.get('title','') != exist.title:
                    asyncio.run((Sendmessage(f"Asset Title changed: `{obj.get('url')}` to {obj.get('title')} \nProgram Name: \#{program_name}")))
                if obj.get('status_code',[]) != exist.status_code:
                    asyncio.run((Sendmessage(f"Asset Status Code changed: `{obj.get('url')}` to {obj.get('status_code')} \nProgram Name: \#{program_name}")))
                exist.ips = obj.get('a',[])
                exist.tech = obj.get('tech',[])
                exist.favicon = obj.get('favicon','')
                exist.title = obj.get('title','')
                exist.status_code = obj.get('status_code',[])
                exist.headers = obj.get('header',[])
                exist.url = obj.get('url','')
                exist.final_url = obj.get('final_url','')
                exist.save()
                print(f'Updated http asset: {obj.get("url")}')
            else:
                new_httpx = HTTPx(programm_name=program_name, 
                                  subdomain=subdomain, 
                                  ips=obj.get('a',[]), 
                                  tech=obj.get('tech',[]), 
                                  favicon=obj.get('favicon',''), 
                                  title=obj.get('title',''), 
                                  status_code=obj.get('status_code',[]),
                                  headers=obj.get('header',[]),
                                  url=obj.get('url',''),
                                  final_url=obj.get('final_url',''))
                new_httpx.save()
                print(f'Inserted new http asset: {obj.get("url")}')
                asyncio.run((Sendmessage(f"New HTTP Asset for Work: `{obj.get('url')}`\nProgram Name: \#{program_name}")))

    except Programm.DoesNotExist:
        print("not")



def run_httpx(domain):
    """
    Run httpx command with the given domain and return the output along with its length.
    """
    #if check_cdn(domain):
    command = f'echo "https://ooof-ooof.civeb44940.workers.dev/?dieuri=http://{domain}" | /root/go/bin/httpx -silent -json -random-agent -favicon -fhr -tech-detect -irh -include-chain -timeout 5 -retries 3 -threads 5 -rate-limit 4 -ports 443 -extract-fqdn -H "Referer: https://{domain}"'
    #else:
        #command = f'echo {domain} | /root/go/bin/httpx -silent -json -random-agent -favicon -fhr -tech-detect -irh -include-chain -timeout 5 -retries 3 -threads 5 -rate-limit 4 -ports 443,80,1080,1433,1434,4000,4001,4002,8000,8080,8443,8888 -extract-fqdn -H "Referer: https://{domain}"'

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
        output = output.strip().split('\n')
        if output == ['']:
            output = None
            return output
        
        output = [json.loads(json_object) for json_object in output]
        return output
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print(f"Error running command: {e}")
        return None, None



class Command(BaseCommand):
    help = "Run httpx command with the given domain"

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str, help='Domain to run httpx on')

    def handle(self, *args, **options):
        domain = options['domain']
        if get_domain_tld(domain):
            livesubdomains = LiveSubdomains.objects.all().filter(subdomain__endswith=f'.{domain}')
            if livesubdomains:
                for subdomain in livesubdomains:    
                    result = run_httpx(subdomain.subdomain)
                    if result:
                        for item in result:
                            upsert_httpx(check_domain(domain)['program_name'], subdomain.subdomain, item)


        else:
            livesubdomains = LiveSubdomains.objects.all().filter(programm_name=domain)
            if livesubdomains:
                for subdomain in livesubdomains:    
                    result = run_httpx(subdomain.subdomain)
                    if result:
                        for item in result:
                            upsert_httpx(domain, subdomain.subdomain, item)

