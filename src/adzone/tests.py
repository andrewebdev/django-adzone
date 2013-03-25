from datetime import datetime

from django.test import TestCase
# from django.test.client import RequestFactory
from django.contrib.auth.models import User

from adzone.models import Advertiser, AdCategory, AdZone, AdBase
from adzone.models import AdImpression, AdClick
from adzone.managers import AdManager


# Helper functions to help setting up the tests
user = lambda: User.objects.create_user('test', 'test@example.com', 'secret')


def datenow():
    return datetime.now()


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

    def test_manager_exists(self):
        AdManager

    def test_get_random_ad(self):
        self.assertTrue(False)

    def test_get_random_ad_by_category(self):
        self.assertTrue(False)


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

    def test_random_zone_ad(self):
        self.assertTrue(False)

    def test_random_category_ad(self):
        self.assertTrue(False)


class AdViewTestCase(TestCase):

    def test_request_creates_click(self):
        self.assertTrue(False)

    def test_response_redirects_to_ad_url(self):
        self.assertTrue(False)
