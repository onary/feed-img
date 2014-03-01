from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse

from apps.worker.models import Images

# Create your views here.

def index(request):
    page = int(request.GET.get('page', 0))

    if page:
        imgs = Images(page-1).get()
        print len(imgs)
        return render(request, 'items.html', {'images': imgs})

    return render(request, 'base.html')

