from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import HTTPx
from datetime import timedelta


@csrf_exempt
def http_all(request):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(hours=12)
        # Retrieve all Subdomains instances
        http_sv = HTTPx.objects.all().filter(last_update__gte=time_threshold).values()
        return JsonResponse(list(http_sv), safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def http_filter(request , domain):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(hours=12)
        if '.' in domain:
        # Retrieve specific Subdomains instances
            http_sv = HTTPx.objects.all().filter(subdomain__endswith=f'.{domain}', last_update__gte=time_threshold).values()
        else:
            http_sv = HTTPx.objects.all().filter(programm_name=domain, last_update__gte=time_threshold).values()

        return JsonResponse(list(http_sv), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
    


@csrf_exempt
def http_filter_tech(request , tech):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(hours=12)
        http_sv = HTTPx.objects.all().filter(tech__icontains=tech, last_update__gte=time_threshold).values()

        return JsonResponse(list(http_sv), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def http_filter_title(request , title):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(hours=12)
        http_sv = HTTPx.objects.all().filter(title__icontains=title, last_update__gte=time_threshold).values()

        return JsonResponse(list(http_sv), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def http_fresh_all(request):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(days=1)
        # Retrieve all Subdomains instances
        http_sv = HTTPx.objects.all().filter(created_date__gte=time_threshold).values()
        return JsonResponse(list(http_sv), safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def http_fresh_filter(request , domain):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(days=1)
        if '.' in domain:
        # Retrieve specific Subdomains instances
            http_sv = HTTPx.objects.all().filter(subdomain__endswith=f'.{domain}', created_date__gte=time_threshold).values()
        else:
            http_sv = HTTPx.objects.all().filter(programm_name=domain, created_date__gte=time_threshold).values()

        return JsonResponse(list(http_sv), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def http_fresh_filter_tech(request , tech):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(days=1)
        http_sv = HTTPx.objects.all().filter(tech__icontains=tech, created_date__gte=time_threshold).values()

        return JsonResponse(list(http_sv), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def http_fresh_filter_title(request , title):
    if request.method == 'GET':
        time_threshold = timezone.localtime() - timedelta(days=1)
        http_sv = HTTPx.objects.all().filter(title__icontains=title, created_date__gte=time_threshold).values()

        return JsonResponse(list(http_sv), safe=False)  # Return the data as JSON
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)