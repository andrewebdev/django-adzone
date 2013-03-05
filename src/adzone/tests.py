from datetime import datetime

from django.test import TestCase
# from django.test.client import RequestFactory
# from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from adzone.models import Advertiser, AdCategory, AdZone, AdBase


user = lambda: User.objects.create_user('test', 'test@example.com', 'secret')


def datenow():
    return datetime.now()


def create_objects():
    advertiser = Advertiser.objects.create(
        company_name='Advertiser Name 1',
        website='http://example.com/', user=user())

    category = AdCategory.objects.create(
        title='Internet Services',
        slug='internet-services',
        description='All internet based services')

    adzone = AdZone.objects.create(
        title='Sidebar',
        slug='sidebar',
        description='Sidebar Zone Description')

    return advertiser, category, adzone

    # ad = TextAd.objects.create(
    #     title='First Ad',
    #     content='For all your web design and development needs, at competitive rates.',
    #     url='http://www.teh-node.co.za/',
    #     enabled=True,
    #     advertiser=self.advertiser,
    #     category=self.category,
    #     zone=self.adzone)

    # ad2 = TextAd.objects.create(
    #     title='Second Ad',
    #     content='A second advert.',
    #     url='http://www.teh-node.co.za/',
    #     enabled=True,
    #     advertiser=self.advertiser,
    #     category=self.category2,
    #     zone=self.adzone2)

    # ad3 = TextAd.objects.create(
    #     title='A Third Ad',
    #     content='A third advert.',
    #     url='http://www.teh-node.co.za/',
    #     enabled=True,
    #     advertiser=self.advertiser,
    #     category=self.category2,
    #     zone=self.adzone2)

    # # AdImpression Setup
    # impression1 = AdImpression.objects.create(
    #     impression_date=datenow(),
    #     source_ip='127.0.0.2',
    #     ad=self.ad)

    # impression2 = AdImpression.objects.create(
    #     impression_date=datenow(),
    #     source_ip='127.0.0.3',
    #     ad=self.ad2)

    # # Clicks Setup
    # adclick1 = AdClick.objects.create(
    #     click_date=datenow(),
    #     source_ip='127.0.0.1',
    #     ad=self.ad)


class AdvertiserTestCase(TestCase):

    def test_model(self):
        Advertiser(
            company_name='Advertiser Name 1',
            website='http://example.com/',
            user=user())

    def test_get_website_url(self):
        advertiser = Advertiser(
            company_name='Advertiser Name 1',
            website='http://example.com/',
            user=user())

        self.assertEqual(
            'http://example.com/',
            advertiser.get_website_url())


class AdCategoryTestCase(TestCase):

    def test_model(self):
        AdCategory(
            title='Internet Services',
            slug='internet-services',
            description='All internet based services')


class AdZoneTestCase(TestCase):

    def test_model(self):
        AdZone(
            title='Ad Zone Title',
            slug='adzone',
            description='Ad Zone Description')


class AdBaseTestCase(TestCase):

    def test_model(self):
        advertiser, category, zone = create_objects()
        AdBase(
            title='Ad Title',
            url='www.example.com',
            advertiser=advertiser,
            category=category,
            zone=zone
        )


# class AdvertTestCase(AdvertisingTestCase):
#     def testAd(self):
#         self.assertEquals(reverse(
#             'adzone_ad_view',
#             args=['1']
#         )[-8:], '/view/1/')
#         adimpressions = AdImpression.objects.filter(ad=self.ad)
#         self.assertEquals(len(adimpressions), 1)
#         self.assertEquals(adimpressions[0].source_ip, '127.0.0.2')
#
#     def testAdAdvertiser(self):
#         self.assertEquals(self.ad.advertiser.__unicode__(), 'teh_node Web Development')
#         self.assertEquals(self.ad.advertiser.company_name, 'teh_node Web Development')
#
#     def testAddsInCategory(self):
#         ads = TextAd.objects.filter(category__slug='internet-services')
#         self.assertEquals(len(ads), 1)
#         self.assertEquals(ads[0].title, 'First Ad')
#
#     def testRandomAd(self):
#         ad = AdBase.objects.get_random_ad(
#             ad_category='internet-services',
#             ad_zone='sidebar'
#         )
#         self.assertEquals(ad.title, 'First Ad')
#
#
# class ImpressionTestCase(AdvertisingTestCase):
#     def testImpression(self):
#         impressions = AdImpression.objects.all()
#         self.assertEquals(len(impressions), 2)
#
#
# class ClickTestCase(AdvertisingTestCase):
#
#     def testClicks(self):
#         clicks = AdClick.objects.all()
#         self.assertEquals(len(clicks), 1)
#
#     def testClickOnAds(self):
#         c = Client(REMOTE_ADDR='127.0.0.1')
#         response = c.get(reverse(
#             'adzone_ad_view',
#             args=['1']
#         ))
#         self.assertEquals(len(AdClick.objects.all()), 2)
#         click = AdClick.objects.all()[1]
#         self.assertEquals(click.source_ip, '127.0.0.1')
#
#     def testInvalidAdURL(self):
#         c = Client(REMOTE_ADDR='127.0.0.1')
#         response = c.get('/te/10')
#         self.assertEquals(len(AdClick.objects.all()), 1)
