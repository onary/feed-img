import urllib2, urllib
from django.core.cache import get_cache
from django.conf import settings
import ast

try:
    import simplejson
except ImportError:
    import json as simplejson


class GoogleImages(object):
    """
    1) Represents a google image search result using Google search API

    https://developers.google.com/image-search/v1/jsondevguide#json_response

    Note: The Image Searcher supports a maximum of 8 result pages. 
          When combined with subsequent requests, a maximum total of 64 results are available. 
          It is not possible to request more than 64 results.

    2) Caches data on key 'title' (optional)

    3) Able to search recent result in cache by query
    """

    def __init__(self, page=0, query="Funny images", start=0, rsz=8, 
                 basicUrl='https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=',
                 cycles=2, cache=False):

        self.page = page
        self.query = query
        self.start = start
        self.rsz = rsz
        self.basicUrl = basicUrl
        self.cycles = cycles
        self.cache = cache or get_cache('redis_cache.cache.RedisCache', 
                                        **settings.CACHES['default'])


    def get(self, request=None, domen=['tumblr.com', 'instagram.com'], ref='/'):
        """
        Makes a request to the Google API
        and call cache method (optional)

        example of result:
        [{"GsearchResultClass":"GimageSearch",
        "width":"597",
        "height":"622",
        "imageId":"ANd9GcSTZXO7kuDGARx9kS97AUJZ5GgFyOsrytjwCh-HpT8nNCDIRMrz-25G1eCD",
        "tbWidth":"131",
        "tbHeight":"136",
        "unescapedUrl":"http://community.us.playstation.com/t5/original?v\u003dmpbl-1\u0026px\u003d-1",
        "url":"http://community.us.playstation.com/t5/image/original.jpg",
        "visibleUrl":"community.us.playstation.com",
        "title":"\u003cb\u003eFunny\u003c/b\u003e Pictures - Page 2 - PlayStation® Forums",
        "titleNoFormatting":"Funny Pictures - Page 2 - PlayStation® Forums",
        "originalContextUrl":"http://community.us.playstation.com/Funny-Pictures/td-p/39995049/page/2",
        "content":"\u003cb\u003efunny\u003c/b\u003e-christmas-humor-\u003cb\u003efunny\u003c/b\u003e-",
        "contentNoFormatting":"funny-christmas-humor-funny-",
        "tbUrl":"http://t2.gstatic.com/images?qFyOsrytjwCh-HpT8nNCDIRMrz-25G1eCD"
        },
        {
            ...
            ...
        }]
        """
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
                            self.url(cycle), None, {'Referer': ref})
                            )
                        )['responseData']['results'])
                except Exception, e:
                    pass

        if request:
            self.cache_result(results, request)

        return results


    def url(self, cycle=1, site=None):
        """
        forms URL for google API request
        """
        query = self.normalize_query(self.query)
        domen = ('&as_sitesearch=%s' % site) if site else ""
        rsz = '&rsz=%s' % self.rsz
        start = '&start=%s' % (self.start if self.start else \
            (self.page * self.cycles + cycle - 1) * self.rsz)

        return self.basicUrl + query + domen + rsz + start


    def normalize_query(self, query):
        return query.strip().replace(":", "%3A").replace("+", "%2B")\
                .replace("&", "%26").replace(" ", "+").lower()


    def cache_result(self, results, request, timeout=60*10):
        """
        Write in cache (Redis) bunch of latest results
        """
        token = request.session.get('token')
        for res in results:
            key = '%s:%s:%s' % (token, 
                self.normalize_query(res['title']), res['imageId'][:15])
            self.cache.set(key, str(res), timeout=timeout)


    def search(self, request):
        """
        Withdraw latest results from cache by query
        """
        query = self.normalize_query(request.GET.get('q', ''))
        results = []
        if query:
            token = request.session.get('token')
            keys = self.cache.keys('%s*' % token)

            keys_list = []
            for key in keys:
                if key[11:-16].find(query) != -1:
                    keys_list.append(key)

            for key in keys_list:
                results.append(ast.literal_eval(self.cache.get(key)))

        return results
