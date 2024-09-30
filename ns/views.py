from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import LiveSubdomains
from subenum.models import Subdomains
from datetime import timedelta
from django.utils import timezone


@csrf_exempt
def live_all(request):
    if request.method == 'GET':
        time_threshold = timezone.now() - timedelta(hours=12)
        # Retrieve all Subdomains instances
        subdomains = LiveSubdomains.objects.all().filter(last_update__gte=time_threshold).values()
        return JsonResponse(list(subdomains), safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
    


@csrf_exempt
def live_filter(request , domain):
    if request.method == 'GET':
        time_threshold = timezone.now() - timedelta(hours=12)
        if '.' in domain:
        # Retrieve specific Subdomains instances
            subdomains = LiveSubdomains.objects.all().filter(subdomain__endswith=f'.{domain}', last_update__gte=time_threshold).values()
        else:
            subdomains = LiveSubdomains.objects.all().filter(programm_name=domain, last_update__gte=time_threshold).values()

        return JsonResponse(list(subdomains), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def live_fresh_all(request):
    if request.method == 'GET':
        time_threshold = timezone.now() - timedelta(days=1)
        # Retrieve all Subdomains instances
        subdomains = LiveSubdomains.objects.all().filter(created_date__gte=time_threshold).values()
        return JsonResponse(list(subdomains), safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def live_fresh_filter(request , domain):
    if request.method == 'GET':
        time_threshold = timezone.now() - timedelta(days=1)
        if '.' in domain:
        # Retrieve specific Subdomains instances
            subdomains = LiveSubdomains.objects.all().filter(subdomain__endswith=f'.{domain}', created_date__gte=time_threshold).values()
        else:
            subdomains = LiveSubdomains.objects.all().filter(programm_name=domain, created_date__gte=time_threshold).values()

        return JsonResponse(list(subdomains), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
    


@csrf_exempt
def live_provider_filter(request , provider):
    if request.method == 'GET':
        time_threshold = timezone.now() - timedelta(hours=12)
        # Retrieve all Subdomains instances
        subdomains = Subdomains.objects.all().filter(providers=[provider]).values()
        live_subdomains = []
        for subdomain in subdomains:
            print(subdomain['subdomain'])
            lives = LiveSubdomains.objects.all().filter(subdomain=subdomain['subdomain'], created_date__gte=time_threshold).values()
            if lives:
                live_subdomains.append(list(lives)[0])
        return JsonResponse(live_subdomains, safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)