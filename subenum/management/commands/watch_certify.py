import subprocess , os , tldextract , socket , ssl , re
from django.core.management.base import BaseCommand
from cryptography import x509
from cryptography.hazmat.backends import default_backend
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



def run_certify(domain):
    """
    Run certify function with the given domain and return the output along with its length.
    """
    output = []
    
    # Create an SSL context and disable hostname verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        # Connect to the server and retrieve the certificate
        with socket.create_connection((domain, 443) , timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                # Get the server's certificate in DER format and convert it to PEM
                cert = ssock.getpeercert(True)
                pem_cert = ssl.DER_cert_to_PEM_cert(cert)

        # Load the certificate
        cert = x509.load_pem_x509_certificate(pem_cert.encode(), default_backend())

        # Extract the Common Name (CN) from the Subject
        subject_cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        output.append(subject_cn)

        # Extract the Subject Alternative Name (SAN) values
        san_extension = cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        san_dns_names = san_extension.value.get_values_for_type(x509.DNSName)
        for dns in san_dns_names:
            output.append(dns)
    except:
        pass

        return output



class Command(BaseCommand):
    help = "Run certify command with the given domain"

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str, help='Domain to run certify on')

    def handle(self, *args, **options):
        domain = options['domain']
        result = run_certify(domain)
        if result:
            for sub in result:
                sub = sub.replace('*.', '')
                if sub == domain or sub == 'www.'+domain or sub == get_domain_tld(domain):
                    continue
                else:
                    upsert_subdomain(check_domain(domain)['program_name'] , sub , 'certify')