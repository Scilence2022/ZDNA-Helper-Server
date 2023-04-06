#from django.http import HttpResponse
from django.shortcuts import render

def zdna(request):
    context = {}
    context['title'] = 'A demo helper server for NFT metadata encryption password updating'
    return render(request, 'TPZDNA.html', context)

