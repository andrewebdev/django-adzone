from django.test import TestCase
from models import Advertiser, Ad, AdView, AdClick, AdCategory, AdZone
from models import priority_ads
from django.contrib.auth.models import User

def datenow():
    from datetime import datetime
    return datetime.now()

class AdvertingTestCase(TestCase):
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
        self.ad = Ad.objects.create(
                title = 'First Ad',
                content = 'For all your web design and development needs, at competitive rates.',
                url = 'http://www.teh-node.co.za/',
                enabled = True,
                since = datenow(),
                updated = datenow(),
                advertiser = self.advertiser,
                category = self.category,
                zone = self.adzone)

        self.ad2= Ad.objects.create(
                title = 'Second Ad',
                content = 'A second advert.',
                url = 'http://www.teh-node.co.za/',
                enabled = True,
                since = datenow(),
                updated = datenow(),
                advertiser = self.advertiser,
                category = self.category2,
                zone = self.adzone2)

        self.ad3= Ad.objects.create(
                title = 'A Third Ad',
                content = 'A third advert.',
                url = 'http://www.teh-node.co.za/',
                enabled = True,
                since = datenow(),
                updated = datenow(),
                advertiser = self.advertiser,
                category = self.category2,
                zone = self.adzone2)

      # Views Setup
        self.adview1 = AdView.objects.create(
                ad = self.ad,
                view_date=datenow(),
                view_ip='127.0.0.1')
        self.adview2 = AdView.objects.create(
                ad = self.ad,
                view_date=datenow(),
                view_ip='111.1.1.8')

        # Clicks Setup
        self.adclick1 = AdClick.objects.create(
                ad=self.ad,
                click_date=datenow(),
                click_ip='127.0.0.1')
        
    def testAdvertiser(self):
        self.assertEquals(self.advertiser.get_website_url(), 'http://andre.smoenux.webfactional.com/')

    def testAd(self):
        self.assertEquals(self.ad.get_ad_url(), 'http://www.teh-node.co.za/')

    def testAdViews(self):
        self.ad.view('222.0.3.45')
        self.assertEquals(len(self.ad.adview_set.all()), 3)
        self.assertEquals(self.ad.adview_set.all()[2].view_ip, '222.0.3.45')

    def testAdClicks(self):
        self.ad.click('222.0.3.45')
        self.assertEquals(len(self.ad.adclick_set.all()), 2)
        self.assertEquals(self.ad.adclick_set.all()[1].click_ip, '222.0.3.45')

    def testAdAdvertiser(self):
        self.assertEquals(self.ad.advertiser.__unicode__(), 'teh_node Web Development')
        self.assertEquals(self.ad.advertiser.company_name, 'teh_node Web Development')

    def testAddsInCategory(self):
        ads = Ad.objects.filter(category__slug='internet-services')
        self.assertEquals(len(ads), 1)
        self.assertEquals(ads[0].title, 'First Ad')

    def testAdView(self):
        self.assertEquals(self.adview1.__unicode__(), 'First Ad')

    def testAdClick(self):
        self.assertEquals(self.adclick1.__unicode__(), 'First Ad')

    def testAdCategory(self):
        self.assertEquals(self.category.__unicode__(), 'Internet Services')

    def testAdZone(self):
        self.assertEquals(self.adzone.__unicode__(), 'Sidebar')

    def testAdinZone(self):
        ads = Ad.objects.filter(zone__slug='sidebar')
        self.assertEquals(len(ads), 1)

    def testPriorityAds(self):
        allads = priority_ads() # Standard
        self.assertEquals(len(allads), 3)
        self.assertEquals(allads[1].title, 'Second Ad')

        allads = priority_ads(by_views=True)
        self.assertEquals(len(allads), 3)

        sidebarads = priority_ads(Ad.objects.filter(zone__slug='sidebar'), by_views=True, ad_count=2)
        self.assertEquals(len(sidebarads), 1)
        self.assertEquals(sidebarads[0].title, 'First Ad')
