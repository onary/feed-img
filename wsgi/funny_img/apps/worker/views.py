import random
import string
import time
from datetime import datetime

from urlparse import parse_qs

from django.conf import settings
from django.shortcuts import render

from instagram.client import InstagramAPI
from apps.worker.models import GoogleImages
from pytumblr import TumblrRestClient


# creating client for tumbler
tumblr_client = TumblrRestClient(consumer_key=settings.TUMBLR_KEY, 
    consumer_secret=settings.TUMBLR_SECRET)

# creating client for instagram
inst_client = InstagramAPI(client_id=settings.INSTAGRAM_ID)


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
    items, next_url = inst_client.tag_recent_media(30, max_id, 'funny')
    request.session['page%s' % (page +1)] = parse_qs(next_url)['max_tag_id'][0]

    if page:
        return render(request, 'instagram_items.html', {'items': items})

    return render(request, 'instagram.html', {'items': items})


def tumblr(request):
    page = int(request.GET.get('page', 0))
    if not page: 
        request.session['time'] = time.mktime(datetime.now().timetuple())
    
    # Using timestamp object for pagination
    items = tumblr_client.tagged("funny", limit=20, 
        before=(request.session.get('time', 1394041341) - page * 60 * 10)
        )

    if page:
        return render(request, 'tumblr_items.html', {'items': items})

    return render(request, 'tumblr.html', {'items': items})
