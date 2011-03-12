from django.http import HttpResponse


def home(request):
    return HttpResponse('hello world', content_type='text/plain')
