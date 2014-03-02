import urllib2, urllib
from django.core.cache import get_cache
from django.conf import settings
import ast

try:
    import simplejson
except ImportError:
    import json as simplejson


class Images(object):
    def __init__(self, 
                page=0, 
                query="Funny images", 
                start=0, 
                rsz=8, 
                basicUrl='https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=',
                cycles=2):

        self.page = page
        self.query = query
        self.start = start
        self.rsz = rsz
        self.basicUrl = basicUrl
        self.cycles = cycles
        self.cache = get_cache('redis_cache.cache.RedisCache', **settings.CACHES['default'])

    def get(self, request=None, domen=['tumblr.com', 'instagram.com'], ref='/'):
        results = []
        for cycle in range(1, self.cycles + 1):
            if domen:
                for site in domen:
                    try:
                        results += list(simplejson.load(
                            urllib2.urlopen(urllib2.Request(
                                self.url(cycle, site), None, {'Referer': ref})
                                )
                            )['responseData']['results'])
                    except Exception, e:
                        pass
            else:
                try:
                    results += list(simplejson.load(
                        urllib2.urlopen(urllib2.Request(
                            self.url(cycle, site), None, {'Referer': ref})
                            )
                        )['responseData']['results'])
                except Exception, e:
                    pass

        if request:
            self.cache_result(results, request)

        return results

    def url(self, cycle=1, site=None):
        query = self.normalize_query(self.query)
        domen = ('&as_sitesearch=%s' % site) if site else ""
        rsz = '&rsz=%s' % self.rsz
        start = '&start=%s' % (self.start if self.start else \
            (self.page * self.cycles + cycle - 1) * self.rsz)

        return self.basicUrl + query + domen + rsz + start

    def normalize_query(self, query):
        return query.strip().replace(":", "%3A").replace("+", "%2B")\
                .replace("&", "%26").replace(" ", "+").lower()

    def cache_result(self, results, request):
        token = request.session.get('token')
        for res in results:
            key = '%s:%s' % (token, self.normalize_query(res['title']))
            self.cache.set(key, str(res), timeout=60*10)

    def search(self, request):
        query = self.normalize_query(request.GET.get('q', ''))
        results = []
        if query:
            token = request.session.get('token')
            keys = self.cache.keys('%s*' % token)

            keys_list = []
            for key in keys:
                if key[11:].find(query) != -1:
                    keys_list.append(key)

            for key in keys_list:
                results.append(ast.literal_eval(self.cache.get(key)))

        return results
