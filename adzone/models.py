# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.db import models
from django.contrib.auth.models import User

def datenow():
    """Just s quick function to return the current date and time"""
    from datetime import datetime
    return datetime.now()

class Advertiser(models.Model):
    """ A Model for our Advertiser
    """
    company_name = models.CharField(max_length=255)
    website = models.URLField(verify_exists=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s" % self.company_name

    def get_website_url(self):
        return "%s" % self.website

class AdCategory(models.Model):
    """ a Model to hold the different Categories for adverts
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Ad Category'
        verbose_name_plural = 'Ad Categories'

    def __unicode__(self):
        return "%s" % self.title

class AdZone(models.Model):
    """ a Model that describes the attributes and behaviours of ad zones
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()

    class Meta:
        verbose_name = 'Ad Zone'
        verbose_name_plural = 'Ad Zones'

    def __unicode__(self):
        return "%s" % self.title

class AdBase(models.Model):
    """ Our basic Advert Model
    """
    title = models.CharField(max_length=255)
    url = models.URLField(verify_exists=True)
    enabled = models.BooleanField(default=False)
    since = models.DateTimeField(default=datenow())
    updated = models.DateTimeField(editable=False)
    # Relations
    advertiser = models.ForeignKey(Advertiser)
    category = models.ForeignKey(AdCategory)
    zone = models.ForeignKey(AdZone)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated = datenow()
        super(AdBase, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.title

    def get_ad_url(self):
        return self.url

class TextAd(AdBase):
    """ A Text based Ad
    """
    content = models.TextField()

class BannerAd(AdBase):
    """ A standard banner Ad
    """
    content = models.ImageField(upload_to="adzone/bannerads/")

class FlashAd(AdBase):
    """ A Flash based ad
    """
    content = models.FileField(upload_to="adzone/flashads/")

class AdView(models.Model):
    """ The AdView Model will record every view that the ad has
    """
    view_date = models.DateTimeField(default=datenow())
    view_ip = models.IPAddressField()

    class Meta:
        verbose_name = 'Ad View'
        verbose_name_plural = 'Ad Views'

    def __unicode__(self):
        return "%s" % self.ad

class AdClick(models.Model):
    """ The AdClick model will record every click that a add gets
    """
    click_date = models.DateTimeField(default=datenow())
    click_ip = models.IPAddressField()

    class Meta:
        verbose_name = 'Ad Click'
        verbose_name_plural = 'Ad Clicks'

    def __unicode__(self):
        return "%s" % self.ad
