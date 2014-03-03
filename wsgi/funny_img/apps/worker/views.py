import random
import string

from django.shortcuts import render
from apps.worker.models import GoogleImages


def make_token(L = 10):
    return ''.join(random.choice(string.ascii_uppercase + 
        string.digits) for _ in range(L))


def index(request):
    page = int(request.GET.get('page', 0))

    if request.GET.get('q', 0):
        return render(request, 'base.html', 
            {'images': GoogleImages().search(request)})

    if page:
        return render(request, 'items.html', 
            {'images': GoogleImages(page).get(request)})

    request.session['token'] = make_token()
    return render(request, 'base.html', 
        {'images': GoogleImages().get(request)})
