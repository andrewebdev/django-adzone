from django.test import TestCase
from models import Advertiser, Ad, AdView, AdClick
from django.contrib.auth.models import User

def datenow():
    from datetime import datetime
    return datetime.now()

class AdvertiserTestCase(TestCase):
    def setUp(self):
        testuser = User.objects.create_user('test', 'test@example.com', 'testpass')

        self.advertiser = Advertiser.objects.create(
                company_name = 'teh_node Web Development',
                website = 'http://andre.smoenux.webfactional.com/',
                user = testuser)

        self.ad = Ad.objects.create(
                title = 'Professional Web Design and Development',
                content = 'For all your web design and development needs, at competitive rates.',
                url = 'http://www.teh-node.co.za/',
                enabled = True,
                since = datenow(),
                updated = datenow(),
                advertiser = self.advertiser
                )

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
        self.ad.view('222.0.3.45')
        self.assertEquals(len(self.ad.adview_set.all()), 3)
        self.assertEquals(self.ad.adview_set.all()[2].view_ip, '222.0.3.45')
        self.ad.click('222.0.3.45')
        self.assertEquals(len(self.ad.adclick_set.all()), 2)
        self.assertEquals(self.ad.adclick_set.all()[1].click_ip, '222.0.3.45')

    def testAdView(self):
        self.assertEquals(self.adview1.__unicode__(), 'Professional Web Design and Development')

    def testAdClick(self):
        self.assertEquals(self.adclick1.__unicode__(), 'Professional Web Design and Development')
