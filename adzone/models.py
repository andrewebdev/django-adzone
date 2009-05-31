# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.db import models

class AddBase(models.Model):
    """ Our abstract Base Model which contains fields and methods for all others
    """
    advertiser = models.ForeignKey('Advertiser', related_name='ads')
    title = models.CharField(max_length=255,
            help_text='A short, descriptive title for the advert')
    url = models.URLField(verify_exists=True,
            help_text='URL that links to the advertiser website')

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True # So that django doesn't create database tables

class TextAdd(AddBase):
    """ A simple text based advert
    """
    shortadd = models.CharField(max_length=255,
            help_text='The short version of the advert')
    longadd = models.TextField(
            help_text='The long version of the advert')

class ImageAdd(AddBase):
    """ A Image based add
    """
    picture = models.ImageField(upload_to="adverts/images/")

class FlashAdd(AddBase):
    """ A Flash animation
    """
    flashfile = models.FileField(upload_to="adverts/flash/")

class Advertiser(models.Model):
    """ A single advertiser and related information
    """
    company_name = models.CharField(max_length=255,
            help_text="The company name of the advertiser")
    contact_first_name = models.CharField(max_length=255,
            help_text="The first name for the company contact")
    contact_last_name = models.CharField(max_length=255,
            help_text="The last name for the company contact")
    contact_email = models.EmailField(
            help_text="The email for the company contact")

    # The advers related to this advertiser
    ads
