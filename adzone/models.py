# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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

class AdImpression(models.Model):
    """ The AdImpression Model will record every time the ad is loaded on a page
    """
    impression_date = models.DateTimeField(default=datenow())
    source_ip = models.IPAddressField()
    # Set up our content type 
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Ad Impression'
        verbose_name_plural = 'Ad Impressions'

class AdClick(models.Model):
    """ The AdClick model will record every click that a add gets
    """
    click_date = models.DateTimeField(default=datenow())
    source_ip = models.IPAddressField()
    # Set up our content type 
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Ad Click'
        verbose_name_plural = 'Ad Clicks'

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
    impressions = generic.GenericRelation(AdImpression)
    clicks = generic.GenericRelation(AdClick)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated = datenow()
        super(AdBase, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """ This url will redirect to the local view for the ad
            The local view will record the click in the database,
            and then redirect to the actual url the ad was pointing to

            Since we are getting the url for the ad, it means that the
            ad is being shown on a webpage somewhere. So we need to add a
            Impression
        """
        # impression = AdImpression(content_object=self, impression_date=datenow(), source_ip=request.META.get('REMOTE_ADDR'))
        # impression.save()
        return self.id

class TextAd(AdBase):
    """ A Text based Ad
    """
    content = models.TextField()

    def get_absolute_url(self):
        """ Overload to return text ads """
        return "/textad/%s" % super(TextAd, self).get_absolute_url()

class BannerAd(AdBase):
    """ A standard banner Ad
    """
    content = models.ImageField(upload_to="adzone/bannerads/")

    def get_absolute_url(self):
        """ Overload to return bannder ads """
        return "/bannerad/%s" % super(BannerAd, self).get_absolute_url()

class FlashAd(AdBase):
    """ A Flash based ad
    """
    content = models.FileField(upload_to="adzone/flashads/")

    def get_absolute_url(self):
        return "/flashad/%s" % super(FlashAd, self).get_absolute_url()
