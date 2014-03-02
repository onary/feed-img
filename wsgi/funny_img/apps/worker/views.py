from django.shortcuts import render, render_to_response
from django.conf import settings

from apps.worker.models import Images
# from django.core.cache import cache
from django.core.cache import get_cache

from redis_cache import get_redis_connection
# Create your views here.

def get_cache_con():
    return get_cache('redis_cache.cache.RedisCache', **settings.CACHES['default'])

def index(request):
    page = int(request.GET.get('page', 0))

    cache = get_cache_con()
    cache.set('key1', 'blah-blah', timeout=25)
    cache.set('key2', 'blah-blah', timeout=25)
    cache.set('key3', 'blah-blah', timeout=25)
    cache.set('key4', 'blah-blah', timeout=25)

    if page:
        imgs = Images(page).get()
        return render(request, 'items.html', {'images': imgs})

    imgs = Images().get()
    return render(request, 'base.html', {'images': imgs})

def cache_v(request):
    cache = get_cache_con().keys('key*')
    print cache
    return render(request, 'base.html', {'c':cache})
