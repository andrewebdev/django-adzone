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

class Ad(models.Model):
    """ Our basic Advert Model
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    url = models.URLField(verify_exists=True)
    enabled = models.BooleanField(default=False)
    since = models.DateTimeField(default=datenow())
    updated = models.DateTimeField()

    def __unicode__(self):
        return "%s" % self.title

    def get_ad_url(self):
        return self.url
