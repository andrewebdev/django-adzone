from django.test import TestCase
from django.test.client import Client
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse

from adzone.models import *
from django.contrib.auth.models import User

def datenow():
    from datetime import datetime
    return datetime.now()

class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.
    
    Usage:
    
    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})
    
    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client
    
    Once you have a request object you can pass it to any view function, 
    just as if that view had been hooked up using a URLconf.
    
    """
    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'REMOTE_ADDR': '127.0.0.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)

class AdvertisingTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().request()

        self.user = User.objects.create_user('test', 'test@example.com', 'testpass')

        self.advertiser = Advertiser.objects.create(
                company_name = 'teh_node Web Development',
                website = 'http://andre.smoenux.webfactional.com/',
                user = self.user)

        # Categories setup
        self.category = AdCategory.objects.create(
                title = 'Internet Services',
                slug = 'internet-services',
                description = 'All internet based services')

        self.category2 = AdCategory.objects.create(
                title = 'Category Two',
                slug = 'categorytwo',
                description = 'A Second Category')

        # Zones setup
        self.adzone = AdZone.objects.create(
                title = 'Sidebar',
                slug = 'sidebar',
                description = 'Side Bar Ads')

        self.adzone2 = AdZone.objects.create(
                title = 'Content Banner',
                slug = 'contentbanner',
                description = 'Content Adverts')

        # Ad setup
        self.ad = TextAd.objects.create(
                title = 'First Ad',
                content = 'For all your web design and development needs, at competitive rates.',
                url = 'http://www.teh-node.co.za/',
                enabled = True,
                advertiser = self.advertiser,
                category = self.category,
                zone = self.adzone)

        self.ad2 = TextAd.objects.create(
                title = 'Second Ad',
                content = 'A second advert.',
                url = 'http://www.teh-node.co.za/',
                enabled = True,
                advertiser = self.advertiser,
                category = self.category2,
                zone = self.adzone2)

        self.ad3 = TextAd.objects.create(
                title = 'A Third Ad',
                content = 'A third advert.',
                url = 'http://www.teh-node.co.za/',
                enabled = True,
                advertiser = self.advertiser,
                category = self.category2,
                zone = self.adzone2)

        # AdImpression Setup
        self.impression1 = AdImpression.objects.create(
                impression_date=datenow(),
                source_ip='127.0.0.2',
                ad=self.ad)
        self.impression2 = AdImpression.objects.create(
                impression_date=datenow(),
                source_ip='127.0.0.3',
                ad=self.ad2)

        # Clicks Setup
        self.adclick1 = AdClick.objects.create(
                click_date=datenow(),
                source_ip='127.0.0.1',
                ad=self.ad)
        
class AdvertiserTestCase(AdvertisingTestCase):
    def testAdvertiser(self):
        self.assertEquals(self.advertiser.get_website_url(), 'http://andre.smoenux.webfactional.com/')

class CategoryTestCase(AdvertisingTestCase):
    def testAdCategory(self):
        self.assertEquals(self.category.__unicode__(), 'Internet Services')

class ZoneTestCase(AdvertisingTestCase):
    def testAdZone(self):
        self.assertEquals(self.adzone.__unicode__(), 'Sidebar')

    def testAdinZone(self):
        ads = TextAd.objects.filter(zone__slug='sidebar')
        self.assertEquals(len(ads), 1)

class AdvertTestCase(AdvertisingTestCase):
    def testAd(self):
        self.assertEquals(reverse(
            'adzone_ad_view',
            args=['1']
        )[-8:], '/view/1/')
        adimpressions = AdImpression.objects.filter(ad=self.ad)
        self.assertEquals(len(adimpressions), 1)
        self.assertEquals(adimpressions[0].source_ip, '127.0.0.2')

    def testAdAdvertiser(self):
        self.assertEquals(self.ad.advertiser.__unicode__(), 'teh_node Web Development')
        self.assertEquals(self.ad.advertiser.company_name, 'teh_node Web Development')

    def testAddsInCategory(self):
        ads = TextAd.objects.filter(category__slug='internet-services')
        self.assertEquals(len(ads), 1)
        self.assertEquals(ads[0].title, 'First Ad')

    def testRandomAd(self):
        ad = AdBase.objects.get_random_ad(
            ad_category='internet-services',
            ad_zone='sidebar'
        )
        self.assertEquals(ad.title, 'First Ad')

class ImpressionTestCase(AdvertisingTestCase):
    def testImpression(self):
        impressions = AdImpression.objects.all()
        self.assertEquals(len(impressions), 2)

class ClickTestCase(AdvertisingTestCase):
    def testClicks(self):
        clicks = AdClick.objects.all()
        self.assertEquals(len(clicks), 1)

    def testClickOnAds(self):
        c = Client(REMOTE_ADDR='127.0.0.1')
        response = c.get(reverse(
            'adzone_ad_view',
            args=['1']
        ))
        self.assertEquals(len(AdClick.objects.all()), 2)
        click = AdClick.objects.all()[1]
        self.assertEquals(click.source_ip, '127.0.0.1')

    def testInvalidAdURL(self):
        c = Client(REMOTE_ADDR='127.0.0.1')
        response = c.get('/te/10')
        self.assertEquals(len(AdClick.objects.all()), 1)
