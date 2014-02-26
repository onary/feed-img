from django.shortcuts import render, render_to_response

# Create your views here.

def index(request):
    c = {'text': 'Initial test',}
    return render_to_response('base.html',c)