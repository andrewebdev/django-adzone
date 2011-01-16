# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from adzone.managers import AdManager

class Advertiser(models.Model):
    """
    A Model for our Advertiser.
    """

    company_name = models.CharField(verbose_name=_(u'Company Name'), max_length=255)
    website = models.URLField(verbose_name=_(u'Company Site'), verify_exists=(settings.DEBUG==False))
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _(u'Advertiser')
        verbose_name_plural = _(u'Advertisers')
        ordering = ('company_name',)

    def __unicode__(self):
        return self.company_name

    def get_website_url(self):
        return self.website

class AdCategory(models.Model):
    """
    a Model to hold the different Categories for adverts

    """
    title = models.CharField(verbose_name=_(u'Title'), max_length=255)
    slug = models.SlugField(verbose_name=_(u'Slug'), unique=True)
    description = models.TextField(verbose_name=_(u'Description'))

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('title',)

    def __unicode__(self):
        return self.title

class AdZone(models.Model):
    """
    a Model that describes the attributes and behaviours of ad zones

    """
    title = models.CharField(verbose_name=_(u'Title'), max_length=255)
    slug = models.SlugField(verbose_name=_(u'Slug'))
    description = models.TextField(verbose_name=_(u'Description'))

    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
        ordering = ('title',)

    def __unicode__(self):
        return self.title

class AdBase(models.Model):
    """
    This is our base model, from which all ads will inherit.
    The manager methods for this model will determine which ads to
    display return etc.

    """
    title = models.CharField(verbose_name=_(u'Title'), max_length=255)
    url = models.URLField(verbose_name=_(u'Advertised URL'), verify_exists=(settings.DEBUG==False))
    enabled = models.BooleanField(verbose_name=_(u'Enabled'), default=False)
    since = models.DateTimeField(verbose_name=_(u'Since'), default=datetime.now)
    updated = models.DateTimeField(verbose_name=_(u'Updated'), editable=False)

    # Relations
    advertiser = models.ForeignKey(Advertiser)
    category = models.ForeignKey(AdCategory)
    zone = models.ForeignKey(AdZone)

    # Our Custom Manager
    objects = AdManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('adzone_ad_view', [self.id])

    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super(AdBase, self).save(*args, **kwargs)

class AdImpression(models.Model):
    """
    The AdImpression Model will record every time the ad is loaded on a page

    """
    impression_date = models.DateTimeField(verbose_name=_(u'When'), default=datetime.now)
    source_ip = models.IPAddressField(verbose_name=_(u'Who'), null=True, blank=True)
    ad = models.ForeignKey(AdBase)

    class Meta:
        verbose_name = 'Ad Impression'
        verbose_name_plural = 'Ad Impressions'

class AdClick(models.Model):
    """
    The AdClick model will record every click that a add gets

    """
    click_date = models.DateTimeField(verbose_name=_(u'When'), default=datetime.now)
    source_ip = models.IPAddressField(verbose_name=_(u'Who'), null=True, blank=True)
    ad = models.ForeignKey(AdBase)

    class Meta:
        verbose_name = 'Ad Click'
        verbose_name_plural = 'Ad Clicks'

# Example Ad Types
class TextAd(AdBase):
    """ A most basic, text based advert """
    content = models.TextField(verbose_name=_(u'Content'))

class BannerAd(AdBase):
    """ A standard banner Ad """
    content = models.ImageField(verbose_name=_(u'Content'), upload_to="adzone/bannerads/")
