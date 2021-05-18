from django.shortcuts import render

# Create your views here.

def productManager(request):
    context={}
    return render(request, "managers/index.html", context)