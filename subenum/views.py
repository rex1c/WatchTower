from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Subdomains


@csrf_exempt
def subdomain_all(request):
    if request.method == 'GET':
        # Retrieve all Subdomains instances
        subdomains = Subdomains.objects.all().values()
        return JsonResponse(list(subdomains), safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
    


@csrf_exempt
def subdomain_filter(request , domain):
    if request.method == 'GET':
        # Retrieve specific Subdomains instances
        subdomains = Subdomains.objects.all().filter(subdomain__endswith=f'.{domain}').values()

        return JsonResponse(list(subdomains), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
