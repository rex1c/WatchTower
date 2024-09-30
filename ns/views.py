from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import LiveSubdomains


@csrf_exempt
def live_all(request):
    if request.method == 'GET':
        # Retrieve all Subdomains instances
        subdomains = LiveSubdomains.objects.all().values()
        return JsonResponse(list(subdomains), safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
    


@csrf_exempt
def live_filter(request , domain):
    if request.method == 'GET':
        if '.' in domain:
        # Retrieve specific Subdomains instances
            subdomains = LiveSubdomains.objects.all().filter(subdomain__endswith=f'.{domain}').values()
        else:
            subdomains = LiveSubdomains.objects.all().filter(programm_name=domain).values()

        return JsonResponse(list(subdomains), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
