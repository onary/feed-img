import random
import string
from urlparse import parse_qs

from django.conf import settings
from django.shortcuts import render

from instagram.client import InstagramAPI
from apps.worker.models import GoogleImages

api = InstagramAPI(client_id=settings.INSTAGRAM_ID)


def make_token(L = 10):
    return ''.join(random.choice(string.ascii_uppercase + 
        string.digits) for _ in range(L))


def index(request):
    return render(request, 'index.html', {})


def google(request):
    page = int(request.GET.get('page', 0))

    if request.GET.get('q', 0):
        return render(request, 'google.html', 
            {'images': GoogleImages().search(request)})

    if page:
        return render(request, 'google_items.html', 
            {'images': GoogleImages(page).get(request)})

    request.session['token'] = make_token()
    return render(request, 'google.html', 
        {'images': GoogleImages().get(request)})


def instagram(request):
    page = int(request.GET.get('page', 0))
    max_id = request.session.get('page%s' % page, None)
    items, next_url = api.tag_recent_media(20, max_id, 'funny')
    request.session['page%s' % (page +1)] = parse_qs(next_url)['max_tag_id'][0]

    if page:
        return render(request, 'instagram_items.html', {'items': items})

    return render(request, 'instagram.html', {'items': items})