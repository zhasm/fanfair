from django.http import HttpResponse

def index(request):
    sex='pig sex'
    return HttpResponse(sex)

