from django.test import TestCase
from models import Advertiser, AdView, AdClick, AdCategory, AdZone, TextAd, BannerAd, FlashAd
from django.contrib.auth.models import User

def datenow():
    from datetime import datetime
    return datetime.now()

class AdvertisingTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user('test', 'test@example.com', 'testpass')

        self.advertiser = Advertiser.objects.create(
                company_name = 'teh_node Web Development',
                website = 'http://andre.smoenux.webfactional.com/',
                user = testuser)

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

        # Views Setup
        self.adview1 = AdView.objects.create(
                view_date=datenow(),
                view_ip='127.0.0.1')
        self.adview2 = AdView.objects.create(
                view_date=datenow(),
                view_ip='111.1.1.8')

        # Clicks Setup
        self.adclick1 = AdClick.objects.create(
                click_date=datenow(),
                click_ip='127.0.0.1')
        
    def testAdvertiser(self):
        self.assertEquals(self.advertiser.get_website_url(), 'http://andre.smoenux.webfactional.com/')

    def testAdCategory(self):
        self.assertEquals(self.category.__unicode__(), 'Internet Services')

    def testAdZone(self):
        self.assertEquals(self.adzone.__unicode__(), 'Sidebar')

    def testAdinZone(self):
        ads = TextAd.objects.filter(zone__slug='sidebar')
        self.assertEquals(len(ads), 1)

class AdvertTestCase(AdvertisingTestCase):
    def testAd(self):
        self.assertEquals(self.ad.get_ad_url(), 'http://www.teh-node.co.za/')

    def testAdAdvertiser(self):
        self.assertEquals(self.ad.advertiser.__unicode__(), 'teh_node Web Development')
        self.assertEquals(self.ad.advertiser.company_name, 'teh_node Web Development')

    def testAddsInCategory(self):
        ads = TextAd.objects.filter(category__slug='internet-services')
        self.assertEquals(len(ads), 1)
        self.assertEquals(ads[0].title, 'First Ad')
