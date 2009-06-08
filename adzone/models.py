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

class Ad(models.Model):
    """ Our basic Advert Model
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    url = models.URLField(verify_exists=True)
    enabled = models.BooleanField(default=False)
    since = models.DateTimeField(default=datenow())
    updated = models.DateTimeField()
    # Relations
    advertiser = models.ForeignKey(Advertiser)
    category = models.ForeignKey(AdCategory)
    zone = models.ForeignKey(AdZone)

    # Adding these two hidden fields, for the priorityads function.
    # This temporary solution that works. Hopefully django 1.1 will be released soon
    # and then we can remove this :)
    views = models.IntegerField(editable=False, default=0)
    clicks = models.IntegerField(editable=False, default=0)

    def __unicode__(self):
        return "%s" % self.title

    def get_ad_url(self):
        return self.url

    def view(self, from_ip):
        """ method called when the ad is shown on a webpage
            from_ip should be valid ip string ie. '127.0.0.1'
        """
        adview = AdView.objects.create(
                ad=self,
                view_date=datenow(),
                view_ip=from_ip)

    def click(self, from_ip):
        """ method called when the ad is clicked
            from_ip should be valid ip string ie. '127.0.0.1'
        """
        adclick = AdClick.objects.create(
                ad=self,
                click_date=datenow(),
                click_ip=from_ip)

    def get_clicks(self):
        """ Method to return the number of clicks for the ad
        """
        return self.adclick_set.all().count()

    def get_views(self):
        """ Method to return the number of views for the ad
        """
        return self.adview_set.all().count()

    # TODO: The following is messy, remove once Django 1.1 is stable and released
    def update_clicks_views(self):
        """ update the number of clicks and views, for use with the priority ads function
        """
        self.clicks = self.get_clicks()
        self.views = self.get_views()

class AdView(models.Model):
    """ The AdView Model will record every view that the ad has
    """
    ad = models.ForeignKey(Ad)
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
    ad = models.ForeignKey(Ad)
    click_date = models.DateTimeField(default=datenow())
    click_ip = models.IPAddressField()

    class Meta:
        verbose_name = 'Ad Click'
        verbose_name_plural = 'Ad Clicks'

    def __unicode__(self):
        return "%s" % self.ad

def priority_ads(ad_list, by_views=False, by_clicks=False, ad_count=5):
    """ This method will return adds by prioritising them by clicks or views
    """
    if not ad_list: return False
    if by_views:
        try: # Django 1.1 ??
            return ad_list.annotate(num_views=Count('adview_set')).order_by('num_views')[0:ad_count]
        except:
            return ad_list.order_by('views')[0:ad_count]
    elif by_clicks:
        try: # Django 1.1 ??
            return ad_list.annotate(num_clicks=Count('adclick_set')).order_by('num_clicks')[0:ad_count]
        except:
            return ad_list.order_by('clicks')[0:ad_count]
    else: return ad_list[0:ad_count]
