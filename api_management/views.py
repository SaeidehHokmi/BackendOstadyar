#from django.http import HttpResponse
#from django.template import loader

#class HomePage(View):
#    template = loader.get_template('index.html')
#    return HttpResponse(template.render())
        
from django.shortcuts import render
from django.http import HttpResponse

def master(request):
    return HttpResponse("Hello world!")