# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.db import models

def datetimenow():
    """Just s quick function to return the current date and time"""
    from datetime import datetime
    return datetime.datetime.now()

class Ad(models.Model):
    """ Our standard Ad Model
    """
    title = models.CharField(max_length=255,
            help_text='A short title for the ad')
    content = models.TextField(
            help_text='The text based content for the ad')
    url = models.URLField(verify_exists=True,
            help_text='The url to which the advert points')
    advertiser = models.ForeignKey('Advertiser')
    words = models.TextField(
            help_text='a couple of words to describe the advert')
    enabled = models.BooleanField(default=False)
    since = models.DateTimeField(default=datetimenow())
    updated = models.DateTimeField()
