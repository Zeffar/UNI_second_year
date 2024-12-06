from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse("Primul raspuns")

def afis_statica(request):
    return HttpResponse("Un text care nu depinde de parametrii din cale")

def afis_dinamica(request, nr,sir,subcale):
    return HttpResponse(f"Numar: {nr} Sir: {sir} Subcale: {subcale}")