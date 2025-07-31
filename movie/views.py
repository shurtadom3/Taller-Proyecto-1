from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
   return render(request, 'home.html', {'name': 'Sara'})

def about(request):
    return HttpResponse('<h2> Welcome to the About Movie Reviews Page</h2>')