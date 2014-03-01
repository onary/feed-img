import urllib2, urllib

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

    def get(self, domen=['tumblr.com', 'instagram.com'], ref='/'):
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

        return results

    def url(self, cycle=1, site=None):
        query = self.normalize_query(self.query)
        domen = ('&as_sitesearch=%s' % site) if site else ""
        rsz = '&rsz=%s' % self.rsz
        start = '&start=%s' % (self.start if self.start else \
            (self.page * self.cycles + cycle - 1) * self.rsz)

        print self.basicUrl + query + domen + rsz + start
        return self.basicUrl + query + domen + rsz + start

    def normalize_query(self, query):
        return query.strip().replace(":", "%3A").replace("+", "%2B")\
                .replace("&", "%26").replace(" ", "+")
