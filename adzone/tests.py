from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template import Template
from django.template.response import SimpleTemplateResponse
from django.utils import timezone

from adzone.models import Advertiser, AdCategory, AdZone, AdBase
from adzone.models import AdImpression, AdClick
from adzone.managers import AdManager
from adzone.templatetags.adzone_tags import random_zone_ad, random_category_ad


# Helper functions to help setting up the tests
user = lambda: User.objects.create_user('test', 'test@example.com', 'secret')


def datenow():
    return timezone.now()


def create_objects():
    """ Simple helper to create advertiser, category and zone """
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


def create_advert():
    """ Simple helper to create a single ad """
    advertiser, category, zone = create_objects()
    ad = AdBase.objects.create(
        title='Ad Title',
        url='www.example.com',
        advertiser=advertiser,
        category=category,
        zone=zone,
    )
    ad.sites = [Site.objects.get_current()]
    return ad


# Now follows the actual tests
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

    urls = 'adzone.urls'

    def test_model(self):
        advertiser, category, zone = create_objects()
        AdBase(
            title='Ad Title',
            url='www.example.com',
            advertiser=advertiser,
            category=category,
            zone=zone
        )

    def test_unicode(self):
        advert = create_advert()
        self.assertEqual('Ad Title', str(advert))

    def test_absolute_url(self):
        advert = create_advert()
        self.assertEqual('/view/1/', advert.get_absolute_url())


class AdManagerTestCase(TestCase):

    def setUp(self):
        # Create two categories and two adverts
        advertiser, category, zone = create_objects()
        category2 = AdCategory.objects.create(
            title='Category 2',
            slug='category-2',
            description='Category 2 description'
        )
        ad1 = AdBase.objects.create(
            title='Ad Title',
            url='www.example.com',
            advertiser=advertiser,
            category=category,
            zone=zone
        )
        ad2 = AdBase.objects.create(
            title='Ad 2 Title',
            url='www.example2.com',
            advertiser=advertiser,
            category=category2,
            zone=zone
        )
        ad1.sites = [Site.objects.get_current()]
        ad2.sites = [Site.objects.get_current()]

    def test_manager_exists(self):
        AdManager

    def test_get_random_ad(self):
        advert = AdBase.objects.get_random_ad('sidebar')
        self.assertIn(advert.id, [1, 2])

    def test_get_random_ad_by_category(self):
        advert = AdBase.objects.get_random_ad('sidebar',
                                              ad_category='category-2')
        self.assertIn(advert.id, [2])


class AdImpressionTestCase(TestCase):

    def test_model(self):
        advert = create_advert()
        AdImpression(
            impression_date=datenow(),
            source_ip='127.0.0.1',
            ad=advert,
        )


class AdClickTestCase(TestCase):

    def test_model(self):
        advert = create_advert()
        AdClick(
            click_date=datenow(),
            source_ip='127.0.0.1',
            ad=advert,
        )


class TemplateTagsTestCase(TestCase):

    def test_random_zone_ad_creates_impression(self):
        create_advert()
        random_zone_ad({'from_ip': '127.0.0.1'}, 'sidebar')
        self.assertEqual(AdImpression.objects.all().count(), 1)

    def test_random_zone_ad_renders(self):
        template = Template("{% load adzone_tags %}{% random_zone_ad 'sidebar' %}")
        response = SimpleTemplateResponse(template)
        response.render()
        self.assertTrue(response.is_rendered)

    def test_random_category_ad_creates_impression(self):
        create_advert()
        random_category_ad(
            {'from_ip': '127.0.0.1'}, 'sidebar', 'internet-services')
        self.assertEqual(AdImpression.objects.all().count(), 1)

    def test_random_category_ad_renders(self):
        template = Template("{% load adzone_tags %}{% random_category_ad 'sidebar' 'internet-services' %}")
        response = SimpleTemplateResponse(template)
        response.render()
        self.assertTrue(response.is_rendered)


class AdViewTestCase(TestCase):

    urls = 'adzone.urls'

    def test_request_redirects(self):
        create_advert()
        response = self.client.get('/view/1/')
        self.assertEqual(response.status_code, 302)

    def test_request_redirect_chain(self):
        create_advert()
        response = self.client.get('/view/1/', follow=True)
        chain = [('http://www.example.com', 302), ]
        self.assertEqual(response.redirect_chain, chain)

    def test_request_creates_click(self):
        create_advert()
        self.client.get('/view/1/')  # dont need response for this test
        self.assertEqual(AdClick.objects.filter(ad__id=1).count(), 1)
