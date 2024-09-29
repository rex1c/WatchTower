from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Programm

@csrf_exempt
def programm_list(request):
    if request.method == 'GET':
        # Retrieve all Programm instances
        programms = Programm.objects.all().values()
        return JsonResponse(list(programms), safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)