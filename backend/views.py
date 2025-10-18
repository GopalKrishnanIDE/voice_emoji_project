from django.http import HttpResponse

def home(request):
    return HttpResponse("Voice Emoji API is running!")
