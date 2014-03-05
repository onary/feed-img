from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from apps.worker.models import GoogleImages

class Object(object):
    pass

class GoogleImagesTest(TestCase):
    """
    Testing GoogleImages model's methods
    """

    def setUp(self):
        self.request = Object()
        setattr(self.request, 'session', {'token': 'F48ZQ6PAH4'})
        setattr(self.request, 'GET', {'q': 'insta'})
        self.gi_instance = GoogleImages()
        self.items = [{'title': 'instagram images', 
                       'imageId': '123456789ABCDFG', 
                       'url': 'http://testblog.com/test1.jpg'}, 
                       {'title': 'tumbler images', 
                       'imageId': '561234789ABCDFG', 
                       'url': 'http://testblog.com/test2.jpg'}]

    def test_normalize_query(self):
        self.assertEqual(
            self.gi_instance.normalize_query("funny images+tumbler&insta:"), 
            'funny+images%2btumbler%26insta%3a'
            )

    def test_cache_and_search(self):
        """
        Testing cache_result() and search() methods
        """
        self.gi_instance.cache_result(self.items, self.request, 60*3)
        self.assertEqual(self.gi_instance.search(self.request), 
            [{'title': 'instagram images', 
             'imageId': '123456789ABCDFG', 
             'url': 'http://testblog.com/test1.jpg'}]
            )

    def test_url(self):
        self.assertEqual(self.gi_instance.url(2, 'tumblr.com'),
            "https://ajax.googleapis.com/ajax/services/search/images\
?v=1.0&q=funny+images&as_sitesearch=tumblr.com&rsz=8&start=8"
        )

    def test_get(self):
        """
        Tests get method
        """
        items16 = self.gi_instance.get(request=None, domen=None)
        self.assertEqual(len(items16), 16)

        items32 = self.gi_instance.get(request=None, domen=['google.com', 'pinterest.com'])
        self.assertEqual(len(items32), 32)


class GoogleViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_pure(self):
        "Testing google view with pure request"
        response = self.client.get(reverse('google'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_request_page(self):
        "Testing google view with ?page in request"
        response = self.client.get(reverse('google') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_request_q(self):
        "Testing google view with ?q in request"
        response = self.client.get(reverse('google') + '?q=insta')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


class InstagramViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_pure(self):
        "Testing instagram view with pure request"
        response = self.client.get(reverse('instagram'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_request_page(self):
        "Testing instagram view with ?page in request"
        response = self.client.get(reverse('instagram') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

class TumblrViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_pure(self):
        "Testing tumblr view with pure request"
        response = self.client.get(reverse('tumblr'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_request_page(self):
        "Testing tumblr view with ?page in request"
        response = self.client.get(reverse('tumblr') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')