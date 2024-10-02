import subprocess , os , tempfile , json , asyncio
from django.core.management.base import BaseCommand
from telegram import Bot
from programms.models import Programm
from subenum.models import Subdomains
from ns.models import LiveSubdomains


TOKEN = '8192757664:AAGGVVFMczQD8r-He6lxByuscsmhc2GVq58'
CHANNEL_ID = '-1002299317030'



async def Sendmessage(message):
    bot = Bot(token=TOKEN)

    # Send a message
    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='MarkdownV2')



def check_domain(domain):
    try:
        programs = Programm.objects.all()
        for program in programs:
            scopes = program.scopes
            if domain in scopes:
                return {'res':1 , 'program_name':program}
    except Programm.DoesNotExist:
        print("not")



def create_tmp(data):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp_file:
        for value in data : 
            tmp_file.write(value+"\n")
        tmp_file.flush()

    return tmp_file



def upsert_lives(program_name, cdn, obj):
    exist = LiveSubdomains.objects.filter(subdomain=obj.get('host')).first()
    if exist:
        differences = [item for item in obj.get('a') if item not in exist.ips]
        if len(differences) !=0:
            exist.ips = obj.get('a')
            exist.cdn = cdn
            exist.save()
            print(f'updated subdomain: {obj.get("host")}')
        else:
            exist.cdn = cdn
            exist.save()
            print(f'updated subdomain: {obj.get("host")}')
    else:
        new_live_subdomain = LiveSubdomains(programm_name=program_name, subdomain=obj.get('host'), cdn=cdn, ips=obj.get('a'))
        new_live_subdomain.save()
        asyncio.run((Sendmessage(f"New Asset for Work: `{obj.get('host')}` \nProgram Name: \#{program_name}")))



def run_cut_cdn(tmp):
    """
    Run cut-cdn command with the given IP addresses and return the output as True/False.
    """
    result = False
    command = f" cut-cdn -i {tmp} -silent"
    try:
        # Determine the current operating system
        if os.name == 'nt':  # Windows
            shell = r'C:\Windows\System32\cmd.exe'
        else:  # Unix-based systems
            shell = '/bin/zsh'

        # Execute the command in the determined shell and capture the output
        output = subprocess.check_output(command, shell=True, executable=shell)
        # Delete the tmp file
        os.remove(tmp)
        # Decode the output from bytes to string
        output = output.decode('utf-8')
        output_length = len(output.splitlines())
        if output_length != 0:
            pass
        else:
            result = True
        return result
    
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print(f"Error running command: {e}")
        return None, None



def run_dnsx(domain, tmp):
    """
    Run dnsx command with the given domain/program name and return the output along with its length.
    """
    command = f" dnsx -l {tmp} -silent -wd {domain} -rl 30 -t 10 -resp -json -r resolver"
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
        output = [json.loads(json_object) for json_object in output]
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
        if '.' in domain:
            if check_domain(domain)['res'] == 1:
                subdomains = Subdomains.objects.all().filter(subdomain__endswith=f'.{domain}')
                if subdomains:
                    data = [subdomain.subdomain for subdomain in subdomains]
                    # get result of dnsx
                    output = run_dnsx(domain, create_tmp(data).name) # prepare data for dnsx
                    if output:
                        for item in output:
                            # get result of cut-cdn and add to db
                            upsert_lives(check_domain(domain)['program_name'], run_cut_cdn(create_tmp(item.get('a')).name), item)# prepare data for cut-cdn
                else:
                    print(f'domain {domain} does not exists in watchtower')
        else:
            subdomains = Subdomains.objects.all().filter(programm_name=domain)
            if subdomains:
                data = [subdomain.subdomain for subdomain in subdomains]
                # get result of dnsx
                output = run_dnsx(domain, create_tmp(data).name) # prepare data for dnsx
                if output:
                    for item in output:
                        # get result of cut-cdn and add to db
                        upsert_lives(domain, run_cut_cdn(create_tmp(item.get('a')).name), item)# prepare data for cut-cdn
            else:
                print(f'domain {domain} does not exists in watchtower')